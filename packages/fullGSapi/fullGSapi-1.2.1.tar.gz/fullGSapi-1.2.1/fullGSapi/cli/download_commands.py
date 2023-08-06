import click

from pathlib import Path

from fullGSapi.api.client import GradescopeClient

from fullGSapi.cli.utils import LoginTokens, course_id_option, assignment_id_option, get_tokens

@click.command()
@course_id_option
@assignment_id_option
@click.option("--out", "-o", "output", default=None, help="The output file to store the grades.", type=click.Path())
@click.option("--type", "-t", "filetype", default="csv", help="This is the type of file you want to download (csv, xlsx).", type=click.Choice(["csv", "xlsx"]))
@click.pass_context
def download_grades(ctx, course: str, assignment: str, filetype: str, output: str):
    """
    [TA ONLY] Downloads the grades for an assignment.
    """
    tokens: LoginTokens = get_tokens(ctx)
    gs = tokens.gsFullapi

    click.echo(f"Finding assignment...")

    name = gs.get_assignment_name(course, assignment)

    if not name:
        click.echo(f"Failed to find the assignment!")
        return

    click.echo(f"Downloading scores for {name} ({course}, {assignment})...")

    res = gs.download_scores(course, assignment)

    if res:
        if output is None:
            output = "."
        p = Path(output).expanduser().absolute()
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists() and not p.is_file():
            p = p.joinpath(f"{course}.{assignment}.grades.{filetype}")

        with open(p, "wb+") as f:
            f.write(res)
    else:
        click.echo("Failed to download grades!")