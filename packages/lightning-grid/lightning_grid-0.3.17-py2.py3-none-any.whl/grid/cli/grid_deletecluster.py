import click

from grid import Grid


@click.command()
@click.argument('cluster_id', type=str, required=True, nargs=1)
def deletecluster(cluster_id: str) -> None:
    """Deletes cluster"""
    client = Grid()
    if len(cluster_id) == 0:
        raise click.BadArgumentUsage("""
        Pass in cluster, for instance:

        grid deletecluster cluster_id

        """)

    client.delete_cluster(cluster_id=cluster_id[0])
