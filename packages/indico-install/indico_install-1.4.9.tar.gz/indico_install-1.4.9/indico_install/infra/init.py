import click
import pkg_resources

from indico_install.cluster_manager import ClusterManager


def init(location):
    def wrapper():
        """
        Initialize cluster configuration
        """
        template = pkg_resources.resource_filename(location, "cluster.yaml")
        cluster_manager = ClusterManager(input_yaml=template)
        if not cluster_manager.cm_exists:
            click.secho(f"Created Cluster Config", fg="green")
            cluster_manager.save()

    return wrapper
