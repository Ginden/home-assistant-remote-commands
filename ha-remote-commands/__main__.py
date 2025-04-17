import typer

from ha_remote_commands.app_config import AppConfig
from ha_remote_commands.command_server import start_command_server

app = typer.Typer(
    no_args_is_help=True
)


@app.command()
def print_config(env_file: str = '.env') -> None:
    """
    Print the configuration.
    """
    typer.echo("Printing configuration...")
    typer.echo(AppConfig(_env_file=env_file))  # type: ignore


@app.command()
def run(command_dir: str, env_file: str = '.env') -> None:
    """
    Start the command server.
    """
    typer.echo("Running server!")
    start_command_server(command_dir, AppConfig(_env_file=env_file))  # type: ignore


if __name__ == "__main__":
    app()
