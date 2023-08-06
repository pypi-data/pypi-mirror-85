import click
import os
import pathlib
import pickle
import pytz

from datetime import datetime
from dateutil.parser import parse

from fullGSapi.api.client import GradescopeClient
from fullGSapi.api.gs_api_client import GradescopeAPIClient

class LoginTokens:
    def __init__(self, email: str, gsAPI: GradescopeAPIClient, gsFullapi: GradescopeClient):
        self.email = email
        self.gsAPI = gsAPI
        self.gsFullapi = gsFullapi

    def save(self, path: str):
        p = pathlib.Path(path).expanduser().absolute()
        p.parent.mkdir(0o600, parents=True, exist_ok=True)
        with open(p, "wb+") as f:
            pickle.dump(self, f)
        
    @staticmethod
    def load(path: str) -> "LoginTokens":
        with open(pathlib.Path(path).expanduser().absolute(), "rb") as f:
            return pickle.load(f)

login_token_path_option = click.option(
    "--token", "-t", "tokenpath", default="~/.gradescope", help="The path to the token file.", type=click.Path()
)

course_id_option = click.option(
    "--course", "-c", "course", prompt=True, help="This is the Gradescope Course ID.", type=str
)
assignment_id_option = click.option(
    "--assignment", "-a", "assignment", prompt=True, help="This is the Gradescope Assignment ID.", type=str
)

submission_id_option = click.option(
    "--submission", "-s", "submission", prompt=True, help="This is the Gradescope Submission ID.", type=str
)

def get_clients(ctx, path: str, do_login_on_fail: bool=True) -> LoginTokens:
    if pathlib.Path(path).expanduser().absolute().exists():
        print("Found token file! Verifying login...")
        token: LoginTokens = LoginTokens.load(path)
        api_expiration = token.gsAPI.cookie.get("token_expiration_time")
        logged_in = api_expiration and parse(api_expiration) > datetime.now(pytz.UTC) and token.gsFullapi.verify_logged_in()
        if logged_in:
            print(f"Logged in with {token.email}!")
            return token
        else:
            print("You are not logged in!")
    else:
        print(f"Could not find the token '{path}'")
    print("If you would like to login, please follow the prompts.")
    if not do_login_on_fail:
        return False
    lt = None
    from fullGSapi.cli.login import login
    while not lt:
        email = click.prompt("Email", type=str)
        password = click.prompt("Password", hide_input=True, type=str)
        lt = ctx.invoke(login, email=email, password=password, tokenpath=path)
    return lt
    
def get_tokens(ctx):
    ctx.obj["TOKEN"] = get_clients(ctx, ctx.obj["TOKENPATH"])
    return ctx.obj["TOKEN"]

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    if os.path.isfile(dirName):
        return [dirName]
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles