"""Console script for fcust."""
import click
from pathlib import PosixPath
from fcust.fcust import CommonFolder
from fcust.service import (
    create_fcust_service_unit,
    create_user_unit_path,
    activate_service,
    deactivate_service,
)


@click.group()
def main(args=None):
    """Folder Custodian main command"""
    click.echo("Welcome to Fedora Folder Custodian")


@click.command()
@click.argument("folder_path")
def run(
    folder_path: str,
    help="Path where the common foler is located",
):
    """
    Run folder custodian to enforce permissions on specified common folder.
    """

    fpath = PosixPath(folder_path)
    if not fpath.exists():
        raise FileNotFoundError(f"Specified folder {folder_path} does not exist!")

        # assume common folder itself has been created with proper group and permissions.
    click.echo(f"Initiating maintenance on {folder_path}")
    cf = CommonFolder(folder_path=fpath)
    cf.enforce_permissions()
    click.echo("Common folder maintenance completed.")


@click.command()
@click.argument("folder_path")
def setup(
    folder_path: str,
    help="Path where the common foler is located",
):
    """
    Install fcust service for current user.
    """
    fpath = PosixPath(folder_path)
    if not fpath.exists():
        raise FileNotFoundError(f"Specified folder {folder_path} does not exist!")

    click.echo(f"Installing fcust service for {folder_path}")
    unit_path = create_user_unit_path(create_folder=True)
    create_fcust_service_unit(folder_path=fpath, unit_path=unit_path)
    click.echo("fcust service installed.")


@click.command()
def activate():
    """
    Activate fcust service after installing it for current user.
    """
    click.echo("Activating fcust service.")
    activate_service()
    click.echo("fcust service activated.")


@click.command()
def deactivate():
    """
    Deactivate fcust service for current user.
    """
    click.echo("Dectivating fcust service.")
    deactivate_service()
    click.echo("fcust service deactivated.")


main.add_command(run)
main.add_command(setup)
main.add_command(activate)
main.add_command(deactivate)
