import os
import tempfile
import time
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

import typer

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.uploader import Downloader, Uploader
from savvihub.common.constants import ROLETYPE_DATASET_FILES, ROLETYPE_EXPERIMENT_OUTPUT, ROLETYPE_EXPERIMENT_INPUT, \
    DATASET_SOURCE_TYPE_SAVVIHUB
from savvihub.common.utils import parse_str_time_to_datetime

volume_app = typer.Typer()


class PathException(Exception):
    pass


def refine_path(path_arg, raise_if_not_empty=False, raise_if_not_exist=False):
    if path_arg.startswith("savvihub://"):
        return path_arg, True

    path = os.path.abspath(path_arg)
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise PathException(f"Must specify directory: {path_arg}")
        if raise_if_not_empty and len(os.listdir(path)) > 0:
            raise PathException(f"Must specify empty directory: {path_arg}")
    else:
        if raise_if_not_exist:
            raise PathException(f"Must specify directory: {path_arg}")
        os.mkdir(path)

    return path, False


def parse_remote_path(remote_path):
    u = urlparse(remote_path)
    volume_id = u.netloc
    prefix = u.path
    query = parse_qs(u.query)
    snapshot = query.get('snapshot', ['latest'])
    if len(snapshot) != 1:
        typer.echo(f'Invalid snapshots: {remote_path}')
    return volume_id, prefix, snapshot[0]


@volume_app.callback()
def main():
    """
    Manage the mounted volumes
    """
    return


@volume_app.command()
def ls(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, "-r", help="recursive flag"),
):
    """
    List files in the volume with prefix
    """
    def remove_prefix(text, char):
        if text.startswith(char):
            return text[len(char):]
        return text

    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
    except PathException as e:
        typer.echo(str(e))
        return

    volume_id, prefix, snapshot = parse_remote_path(source_path)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    if recursive:
        files = client.volume_file_list(volume_id, snapshot=snapshot, prefix=prefix, recursive='true')
    else:
        files = client.volume_file_list(volume_id, snapshot=snapshot, prefix=prefix, recursive='false')

    for file in files:
        if len(files) == 1 and file.path == remove_prefix(prefix, "/"):  # exact match
            typer.echo(file.path)
        else:
            typer.echo(f'{remove_prefix(remove_prefix(file.path, remove_prefix(prefix, "/")), "/")}')


@volume_app.command()
def describe(
    source_path_arg: str = typer.Argument(...),
):
    """
    Describe the volume information in detail
    """
    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
    except PathException as e:
        typer.echo(str(e))
        return

    volume_id, prefix, _ = parse_remote_path(source_path)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    volume = client.volume_read(volume_id)
    typer.echo(
        f'Volume ID: {volume.id}\n'
        f'Created: {parse_str_time_to_datetime(volume.created_dt)}\n'
        f'Updated: {parse_str_time_to_datetime(volume.updated_dt)}\n'
        f'Type: {volume.role_type}\n'
        f'Workspace:\n'
        f'\tName: {volume.workspace["slug"]}'
    )

    if volume.role_type == ROLETYPE_DATASET_FILES:
        dataset = volume.dataset
        typer.echo(
            f'Dataset:\n'
            f'\tName: {dataset["slug"]}\n'
            f'\tDescription: {dataset["description"]}'
        )

        source = dataset["source"]
        if source["type"] != DATASET_SOURCE_TYPE_SAVVIHUB:
            typer.echo(
                f'\tSource:\n'
                f'\t\tType: {source["type"]}\n'
                f'\t\tPath: {source["bucket_name"]}{source["prefix"]}'
            )
        typer.echo(f'{client.get_full_info_dataset(volume.workspace["slug"], volume.dataset["slug"])}')

    elif volume.role_type == ROLETYPE_EXPERIMENT_OUTPUT or volume.role_type == ROLETYPE_EXPERIMENT_INPUT:
        project = volume.project
        typer.echo(
            f'Project:\n'
            f'\tName: {project["slug"]}\n'
            f'\tDescription: {project["description"]}\n'
            f'\tGit repository: {project["git_http_url_to_repo"]}\n'
            f'{client.get_full_info_project(volume.workspace["slug"], project["slug"])}'
        )

        experiment = volume.experiment
        typer.echo(
            f'Experiment:\n'
            f'\tNumber: {experiment["number"]}\n'
            f'\tStatus: {experiment["status"]}\n'
            f'\tImage: {experiment["kernel_image"]["name"]}\n'
            f'\tResource: {experiment["kernel_resource_spec"]["name"]}\n'
            f'\tCommand: {experiment["start_command"]}\n'
            f'{client.get_full_info_experiment(volume.workspace["slug"], project["slug"], experiment["number"])}'
        )

@volume_app.command()
def rm(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, "-r"),
):
    """
    Remove volume file with path
    """
    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
    except PathException as e:
        typer.echo(str(e))
        return

    volume_id, prefix, snapshot = parse_remote_path(source_path)

    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    file = client.volume_file_read(volume_id, prefix, snapshot)

    if not file:
        typer.echo('[Error] Request entity not found')
        return

    if file.is_dir:
        if not recursive:
            typer.echo('[Error] Remove directory should use -r option')
            return
        deleted_files = client.volume_file_delete(volume_id, prefix, 'true')
    else:
        deleted_files = client.volume_file_delete(volume_id, prefix, 'false')

    if not deleted_files:
        typer.echo('[Error] Server error')
        return

    for file in deleted_files:
        typer.echo(f'{file.path}')

    return


@volume_app.command()
def cp(
    source_path_arg: str = typer.Argument(...),
    dest_path_arg: str = typer.Argument(...),
    watch: bool = typer.Option(False, "-w", "--watch"),
):
    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
        dest_path, is_dest_remote = refine_path(dest_path_arg, raise_if_not_empty=True)
    except PathException as e:
        typer.echo(str(e))
        return

    context = Context()
    client = SavviHubClient(token=context.token)

    hashmap = defaultdict(lambda: "")

    while True:
        if is_source_remote and is_dest_remote:
            # remote -> remote
            source_volume_id, source_prefix, source_snapshot_ref = parse_remote_path(source_path)
            dest_volume_id, dest_prefix, dest_snapshot_ref = parse_remote_path(dest_path)
            if dest_snapshot_ref != 'latest':
                typer.echo(f'Cannot write to snapshots: {dest_path}')
                return
            files = Downloader.get_files_to_download(context, source_volume_id, snapshot=source_snapshot_ref)
            files = [file for file in files if hashmap[file.path] != file.hash]

            if len(files) > 0:
                tmp_dir = tempfile.mkdtemp()
                Downloader.parallel_download(context, tmp_dir, files, progressable=typer.progressbar)
                Uploader.parallel_upload(context, tmp_dir, files, dest_volume_id, progressable=typer.progressbar)

                for file in files:
                    hashmap[file.path] = file.hash

        elif is_source_remote and not is_dest_remote:
            # remote -> local
            source_volume_id, source_prefix, source_snapshot_ref = parse_remote_path(source_path)
            files = Downloader.get_files_to_download(context, source_volume_id, prefix=source_prefix, snapshot=source_snapshot_ref)
            files = [file for file in files if hashmap[file.path] != file.hash]

            typer.echo(f'Find {len(files)} files to download.')
            if len(files) > 0:
                Downloader.parallel_download(context, dest_path, files, progressable=typer.progressbar)

                for file in files:
                    hashmap[file.path] = file.hash

        elif not is_source_remote and is_dest_remote:
            # local -> remote
            dest_volume_id, dest_prefix, dest_snapshot_ref = parse_remote_path(dest_path)
            if dest_snapshot_ref != 'latest':
                typer.echo(f'Cannot write to snapshots: {dest_path}')
                return

            files = Uploader.get_files_to_upload(source_path, hashmap)
            files = [f'{os.path.join(dest_prefix, file)}' for file in files]

            typer.echo(f'Find {len(files)} files to upload.')
            if len(files) > 0:
                Uploader.parallel_upload(context, source_path, files, dest_volume_id, progressable=typer.progressbar)

                hashmap = Uploader.get_hashmap(source_path)
        else:
            typer.echo('Cannot copy volume from local to local')
            return

        if not watch:
            return

        time.sleep(10)
