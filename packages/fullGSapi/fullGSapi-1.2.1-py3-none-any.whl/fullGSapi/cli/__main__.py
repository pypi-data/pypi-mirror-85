import click

from fullGSapi.cli.build import build
from fullGSapi.cli.login import login, check_login
from fullGSapi.cli.download_commands import download_grades
from fullGSapi.cli.submit import submit
from fullGSapi.cli.utils import login_token_path_option

@click.group()
@click.option('--debug/--no-debug', default=False)
@login_token_path_option
@click.pass_context
def cli(ctx: click.Context, debug: bool, tokenpath: str):
    """
    This is the CLI for Gradescope.
    """
    ctx.ensure_object(dict)
    ctx.obj["TOKENPATH"] = tokenpath
    ctx.obj["TOKEN"] = None
    ctx.obj["DEBUG"] = debug


cli.add_command(build)
cli.add_command(login)
cli.add_command(check_login)
cli.add_command(download_grades)
cli.add_command(submit)

if __name__ == '__main__':
    cli()