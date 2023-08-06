import click
import os
import pathlib

from fullGSapi.cli.utils import LoginTokens, course_id_option, assignment_id_option, get_tokens, getListOfFiles

@click.command()
@course_id_option
@assignment_id_option
@click.option("--method", "-m", "method", default="upload", help="The method you are using to submit.", type=click.Choice(["upload", "github", "bitbucket"]))
@click.option("--path", "-p", "path", default=".", help="The file or path which you want to submit", type=click.Path())
@click.option("--repository", "-r", "repository", default=None, help="The full repository path of your repo (must include both the username and repo name).", type=str)
@click.option("--branch", "-b", "branch", default=None, help="The branch which you want to submit.", type=str)
@click.option("--email", "-e", "email", default=None, help="This option allows an instructor to submit an assignment on behalf of some student via their email.", type=str)
@click.option("--leaderboard", "-l", "leaderboard", default="", help="This is the leaderboard name which will show up on Gradescope.", type=str)
@click.option("--programming/--pdf", default=True, help="This is to set if you are submitting a programming vs PDF assignment.", type=bool)
@click.pass_context
def submit(ctx, course: str, assignment: str, method: str, path: str, repository: str, branch: str, email: str, leaderboard: str, programming: bool):
    """
    This allows you to submit a programming or pdf assignment. Instructors may submit on behalf of students.
    """
    
    tokens: LoginTokens = get_tokens(ctx)

    # UPLOAD =================================
    if method == "upload":
        gs = tokens.gsAPI
        if programming:
            click.echo("Collecting files...")
            filenames = getListOfFiles(path)
            files = {f[(len(str(pathlib.Path(path).parent)) if os.path.isfile(path) else len(path)) + 1:]:open(f, 'rb').read() for f in filenames}
            click.echo("Uploading programming submission...")
            res = gs.upload_programming_submission(course, assignment, email, files_dict=files)
        else:
            click.echo("Uploading pdf subission...")
            res = gs.upload_pdf_submission(course, assignment, email, path)
        if res.ok:
            click.echo("Success!")
        else:
            click.echo("Failed!")
            click.echo(res.content)
        return
    if not programming:
        click.echo("Upload is the only method which supports pdf submissions.")
        return
    gs = tokens.gsFullapi

    if not repository:
        click.echo("You must specify a repository if you are not directly uploading files!")
        return
    if not branch:
        click.echo("You must specify the branch you want to upload from!")
        return

    if email is not None:
        res = gs.get_submission_roster(course, assignment)
        if not res:
            click.echo("Failed to fetch the roster! Are you authorized to visit that page?")
            return
        for s in res:
            if s.get("email") == email:
                email = s["id"]
                break
        else:
            click.echo(f"Could not find {email} in the roster!")
            return


    # GITHUB =================================
    if method == "github":
        click.echo("Checking if the repo is valid...")
        data = gs.get_github_projects()
        if not data:
            click.echo("Failed to fetch your GitHub project list! Please go to Gradescope and verify you have authenticated GitHub with your account.")
            return
        repo_id = None
        for repo in data:
            if repo.get("full_name") == repository:
                repo_id = repo["id"]
                break
        else:
            click.echo(f"Could not find the repo {repository} in your account!")
            return
        branches = gs.get_github_branches(repo_id)
        if not branches:
            click.echo(f"Failed to fetch branches for {repository}!")
            return
        for b in branches:
            if b.get("name") == branch:
                break
        else:
            click.echo(f"Could not find the branch '{branch}' in the repository '{repository}'!")
            return
        click.echo("Submitting...")
        if gs.submit_via_repo(course, assignment, method, repo_id, branch, leaderboard_name=leaderboard, owner_id=email):
            click.echo("Success!")
        else:
            click.echo("Failed!")
        return


    # BITBUCKET ==============================
    elif method == "bitbucket":
        data = gs.get_bitbucket_projects()
        if not data:
            click.echo("Failed to fetch your BitBucket project list! Please go to Gradescope and verify you have authenticated BitBucket with your account.")
            return
        for repo in data:
            if repo.get("full_name") == repository:
                break
        else:
            click.echo(f"Could not find the repo {repository} in your account!")
            return
        branches = gs.get_bitbucket_branches(repository)
        if not branches:
            click.echo(f"Failed to fetch branches for {repository}!")
            return
        for b in branches:
            if b.get("name") == branch:
                break
        else:
            click.echo(f"Could not find the branch '{branch}' in the repository '{repository}'!")
            return
        click.echo("Submitting...")
        if gs.submit_via_bitbucket(course, assignment, method, repository, branch, leaderboard_name=leaderboard, owner_id=email):
            click.echo("Success!")
        else:
            click.echo("Failed!")

        return