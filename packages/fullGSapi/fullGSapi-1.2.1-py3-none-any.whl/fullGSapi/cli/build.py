import click

from fullGSapi.cli.utils import assignment_id_option, course_id_option, get_tokens, LoginTokens

@click.command()
@course_id_option
@assignment_id_option
@click.option("--autograder", "-ag", "autograder", default=None, help="The zip file which will build the autograder.", type=click.Path())
@click.option("--image", "-i", "image", default=None, help="This is the dockerhub image name.", type=str)
@click.option("--timeout", "-to", "timeout", default=40*60, help="The defautl timeout of the autograder build.", type=int)
@click.option("--interval", "interval", default=1, help="The defautl interval to check for updates.", type=int)
@click.option("--attach/--rebuild", default=True, help="Reattaches to the build or forces a rebuild of the autograder.", type=bool)
@click.pass_context
def build(ctx, course: str, assignment: str, autograder: str, image: str, timeout: int, interval: int, attach: bool):
    """
    [TA ONLY] Submits a build file to an autograder and rebuilds the autograder.
    """
    tokens: LoginTokens = get_tokens(ctx)
    gs = tokens.gsFullapi

    ag = gs.get_autograder(course, assignment)

    if image:
        if ag.set_manual_configuration(image):
            click.echo("Success!")
        else:
            click.echo("Failed!")
    else:
        if not autograder:
            click.echo("You must supply an autograder or a Dockerhub image!")
            return
        click.echo("Building...")
        if ag.rebuild_and_print_output(autograder, timeout=timeout, check_interval=interval, force_rebuilt=not attach):
            click.echo("Build succeeded!")
        else:
            click.echo("Build failed!")