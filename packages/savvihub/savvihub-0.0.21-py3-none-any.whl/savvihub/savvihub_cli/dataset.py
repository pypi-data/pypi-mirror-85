import typer

dataset_app = typer.Typer()


def parse_dataset_arg(dataset_arg):
    if "/" not in dataset_arg:
        typer.echo("You should specify dataset with workspace. ex) savvihub/mnist")
        return
    workspace, rest = dataset_arg.split("/")
    if ":" in rest:
        dataset, ref = rest.split(":")
    else:
        dataset = rest
        ref = "latest"
    return workspace, dataset, ref


@dataset_app.callback()
def main():
    """
    Manage the collection of data
    """
    return


@dataset_app.command()
def create():
    return


@dataset_app.command()
def read():
    return
