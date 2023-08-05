import click
import untangle
import base64
import json
import re
import sys
from subprocess import Popen, PIPE, STDOUT
from OpenSSL import crypto, SSL
from urllib.error import HTTPError
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser


from indico_install.utils import options_wrapper, run_cmd, convertb64
from indico_install.infra.input_utils import download_indicoapi_data, auth_with_gsutil
from indico_install.kube.svc.restart import restart
from indico_install.infra.single_node import single_node
from indico_install.infra.gke import gke
from indico_install.infra.aks import aks

# Here we try and include the EKS function
# It depends on boto3 which may not be installed
# in which case we include a stub instead
try:
    from indico_install.infra.eks import eks
except Exception:

    @click.command("eks")
    def eks():
        """Not available"""
        pass


@click.group("infra")
@click.pass_context
def infra(ctx):
    """
    Indico infrastructure setup and validation. Supports EKS, GKE, and single node installations.

    EKS Note! must install package with "eks" extras for EKS
    """
    pass


def generate_cert(
    country="US",
    state="MA",
    locality="Boston",
    org="Indico Data Solutions, Inc",
    org_unit="Engineering",
    common_name="indico.io",
    expiration_days=3652,
):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    cert.get_subject().C = country
    cert.get_subject().ST = state
    cert.get_subject().L = locality
    cert.get_subject().O = org
    cert.get_subject().OU = org_unit
    cert.get_subject().CN = common_name

    cert.set_issuer(cert.get_subject())
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(int(expiration_days) * 24 * 60 * 60)

    cert.set_pubkey(key)
    cert.sign(key, "sha512")

    return {
        "crt": crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode(),
        "key": crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode(),
    }


@infra.command("generate-saml")
@click.pass_context
@click.argument("host", required=True, type=str)
@click.argument("metadata_url", required=False, type=str)
@click.option(
    "-f",
    "--custom-saml",
    help="Optional path to a saml settings.json file; if specified, will upload the given file as a noct secret",
)
def generate_saml(ctx, host=None, metadata_url=None, custom_saml=None):
    """
    Generate and inject SAML settings from Azure AD Saml2
    Before running, complete the following steps:
    1. Register the indico platform as an app registration in Azure AD
    2. Add https://<indico IPA hostname>/auth/users/saml/acs" to the web redirection url whitelist

    HOST is the URL of the indico platform
    METADATA_URL is the federation metadata URL

    Example usage:
    indico infra generate-saml app.indico.io https://login.microsoftonline.com/12346-78910-11121314/federationmetadata/2007-06/federationmetadata.xml

    Alternatively, inject a custom settings.json file:
    indico infra generate-saml -f custom-settings.json

    """
    for secret in ["indico-sso-secrets", "indico-sso-cert"]:
        run_cmd(f"kubectl delete secret {secret}")

    crypto_output = generate_cert(common_name=host)

    run_cmd(
        f'''kubectl create secret generic indico-sso-cert --from-literal=sp.key="{crypto_output.get('key')}" --from-literal=sp.crt="{crypto_output.get('crt')}" ''', silent=True
        )

    if custom_saml:
        with open(custom_saml) as settings_file:
            settings = json.load(settings_file)
        settings_content = json.dumps(settings, indent=4)
        run_cmd(
            f'''kubectl create secret generic indico-sso-secrets --from-literal=settings.json='{settings_content}' ''', silent=True
            )
        ctx.invoke(restart, services=["noct"], contains=False, wait="2m")
        return

    # not using custom settings
    if not (host and metadata_url):
        click.secho(
            "Please provide a host and metadata url if not using a custom settings.json file",
            fg="red",
        )
        return
    idp_info = OneLogin_Saml2_IdPMetadataParser.parse_remote(metadata_url)
    jacs = { "url": "https://" + host + "/auth/users/saml/acs", "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" }
    jsls = { "url": "https://" + host + "/auth/users/saml/sls", "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" }
    jsp = { "entityId": "https://" + host + "/auth/users/saml/metadata", "assertionConsumerService": jacs, "singleLogoutService": jsls, "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress" }
    stg = { "strict": "true", "debug": "true", "sp": jsp, "idp": idp_info["idp"] }
    settings_content = json.dumps(stg, indent=4)
    run_cmd(
        f'''kubectl create secret generic indico-sso-secrets --from-literal=settings.json='{settings_content}' ''', silent=True
        )
    ctx.invoke(restart, services=["noct"], contains=False, wait="2m")


@infra.command("download-apidata")
@click.pass_context
@click.argument("version", required=True, type=str)
@click.option(
    "--extract/--no-extract",
    default=True,
    show_default=True,
    help="Automatically extract the downloaded TAR",
)
@options_wrapper()
def download_api_data(ctx, version, *, extract, deployment_root, **kwargs):
    """
    Download VERSION of API data TAR from google cloud to local --deployment-root.
    Un-tar the file into a directory of the same name, also in the deployment-root
    VERSION is something like "v7".

    Requires Authentication with GSutil to download the TAR, but will attempt to auth with an existing key if it exists.

    Will not download TAR if it already exists.
    Will not extract the TAR if the data directory already exists in --deployment-root
    """
    auth_with_gsutil(deployment_root)
    download_indicoapi_data(deployment_root, version=version, extract=extract)


for command_group in [single_node, gke, eks, aks]:
    infra.add_command(command_group)
