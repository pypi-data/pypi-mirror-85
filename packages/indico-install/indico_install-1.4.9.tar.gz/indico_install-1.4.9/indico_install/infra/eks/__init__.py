#!/usr/bin/env python3
from pathlib import Path
from click import secho

import click

from indico_install.infra.init import init
from indico_install.infra.eks import cluster, config, database, network, storage
from indico_install.config import merge_dicts, yaml
from indico_install.utils import run_cmd
from indico_install.cluster_manager import ClusterManager

SOURCES = [network, storage, database, cluster]


@click.group("eks")
@click.pass_context
def eks(ctx):
    """
    Indico infrastructure setup and validation for AWS Kubernetes Service
    """
    ctx.ensure_object(dict)
    ctx.obj["TRACKER"] = ClusterManager()
    if not ((config.access_key and config.access_secret) or config.aws_profile):
        secho("Missing AWS credentials for EKS", fg="yellow")
    else:
        secho(
            f"Using AWS profile: {config.aws_profile}"
            if config.aws_profile
            else f"Using AWS access key: {config.access_key[:5]}****",
            fg="blue",
        )


eks.command("init")(init(__name__))


@eks.command("check")
@click.pass_context
def check(ctx):
    """Validate all resources"""
    try:
        ctx.obj["SESSION"] = config.Session()
    except Exception as e:
        secho(f"AWS Session could not be generated: {e}", fg="red")
        return
    failed = 0
    user_conf = ctx.obj["TRACKER"].cluster_config
    config.ask_for_infra_input(user_conf)
    ctx.obj["TRACKER"].save()
    for resource in SOURCES:
        resource_name = resource.__name__
        secho(f"Validating {resource_name}...")
        try:
            resource.validate(user_conf, session=ctx.obj["SESSION"])
        except Exception as e:
            secho(f"{resource_name} NOT OK! Error: {e}\n", fg="red")
            failed += 1
        else:
            secho(f"{resource_name} OK!\n", fg="green")
    secho(
        f"Validation complete: {failed} errors",
        fg="red" if failed else "green",
        bold=True,
    )


@eks.command("create")
@click.pass_context
@click.option("-f", "--eksctl-file", help="eksctl config file used to create cluster")
@click.option(
    "--enable-cloudwatch", is_flag=True, help="enable application cloudwatch logging"
)
def create(ctx, eksctl_file=None, enable_cloudwatch=False):
    """
    Install the nvidia driver on the cluster
    """
    run_cmd(
        "kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml"
    )
    run_cmd(
        "wget -O v0.3.6.tar.gz https://codeload.github.com/kubernetes-sigs/metrics-server/tar.gz/v0.3.6; tar -xzf v0.3.6.tar.gz; kubectl apply -f metrics-server-0.3.6/deploy/1.8+/"
    )
    user_conf = ctx.obj["TRACKER"].cluster_config

    if not eksctl_file or not Path(eksctl_file).is_file():
        config.ask_for_infra_input(user_conf)
    else:
        with open(eksctl_file, "r") as conf_file:
            conf = yaml.safe_load(conf_file)

        cluster_name = conf["metadata"]["name"]
        region_name = conf["metadata"]["region"]
        user_conf["cluster"] = user_conf.get("cluster", {}) or {}
        user_conf["cluster"]["name"] = cluster_name

        if "public" not in conf["vpc"]["subnets"]:
            user_conf["services"] = merge_dicts(
                user_conf.get("services", {}),
                {
                    "app-edge": {
                        "values": {
                            "annotations": {
                                "service.beta.kubernetes.io/aws-load-balancer-internal": "0.0.0.0/0"
                            },
                            "externalTrafficPolicy": "Cluster",
                        }
                    }
                },
            )
        # optionally enable cloudwatch
        if enable_cloudwatch or conf.get("cloudWatch", False):
            # add policy to node group IAM role
            nodegroups = run_cmd(
                """kubectl get nodes -o json | jq -r '.items[] | .metadata.labels."alpha.eksctl.io/nodegroup-name"' | sort | uniq""",
                silent=True,
            ).splitlines()
            for ng in nodegroups:
                iam_role = run_cmd(
                    f"""aws cloudformation describe-stacks --stack-name eksctl-{cluster_name}-nodegroup-{ng} --no-paginate --query "Stacks[0].Outputs[?OutputKey=='InstanceRoleARN'].OutputValue" --output text""",
                    silent=True,
                ).split("/")[1]
                run_cmd(
                    f"aws iam attach-role-policy --role-name {iam_role} --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy",
                    silent=True,
                )
                # check role assignment
                is_assigned = run_cmd(
                    f"aws iam list-attached-role-policies --role-name {iam_role} | grep CloudWatchAgentServerPolicy",
                    silent=True,
                )
                click.secho(
                    f"CW Agent Policy assigned to {iam_role}", fg="green"
                ) if is_assigned else click.secho(
                    f"CW Agent Policy not assigned to {iam_role}", fg="red"
                )
            # deploy cloudwatch components in amazon-cloudwatch namespace
            run_cmd(
                f"kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cloudwatch-namespace.yaml"
            )
            run_cmd(
                'curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/'
                + cluster_name
                + "/;s/{{region_name}}/"
                + region_name
                + '/" | kubectl apply -f -'
            )
            # check pod deployment
            pods_deployed = run_cmd(
                "kubectl get pods -n amazon-cloudwatch", silent=True
            )
            click.secho(
                "Cloudwatch pods deployed to amazon-cloudwatch namespace", fg="green"
            ) if pods_deployed else click.secho(
                "Cloudwatch pods not deployed to amazon-cloudwatch namespace", fg="red"
            )

    ctx.obj["TRACKER"].save()
