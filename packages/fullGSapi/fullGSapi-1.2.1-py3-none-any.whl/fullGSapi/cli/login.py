import click

from fullGSapi.api.gs_api_client import GradescopeAPIClient
from fullGSapi.api.client import GradescopeClient

from fullGSapi.cli.utils import login_token_path_option, LoginTokens, get_clients

@click.command()
@click.option('--email', '-e', 'email', prompt=True, type=str)
@click.option('--password', '-p', 'password', prompt=True, hide_input=True, type=str)
@login_token_path_option
@click.pass_context
def login(ctx, email: str, password: str, tokenpath: str):
    """
    Logs into Gradescope. Required to use any other command.
    """
    gsapi = GradescopeAPIClient()
    if gsapi.log_in(email, password):
        gs = GradescopeClient()
        if gs.log_in(email, password):
            click.echo(f"Login Successful for {email}!")
            lt = LoginTokens(email, gsapi, gs)
            lt.save(tokenpath)
            return lt
        else:
            click.echo("Failed to login to the frontend API!")
    else:
        click.echo("Failed to login to the official API!")
    return False

@click.command()
@click.pass_context
def check_login(ctx):
    status = get_clients(ctx, ctx.obj["TOKENPATH"])
    if not status:
        click.echo("You are not logged in!")