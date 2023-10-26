import json
from git import Repo, GitCommandError
from sys import platform
import os
# import dotenv that you can load data from .env file
# you need to import python-dotenv package
from dotenv import load_dotenv

# read parameters from .env file
load_dotenv()

# Set your parameters here
# gitlab_token = os.environ.get('GITLAB_TOKEN')
# credentials included in the GitLab repository URL
repo_url = os.environ.get('REPO_URL')
file_path = os.environ.get('FILE_PATH')
commit_message = os.environ.get('COMMIT_MESSAGE')


def change_git_file(repo_url, file_path, commit_message):
    # Clone the repository locally
    repo = Repo.clone_from(repo_url, './temp_repo')

    # Read the contents of the JSON file - TODO REMOVE THIS ON PRODUCTION
    with open(f'./temp_repo/{file_path}', 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        print(data)

    # Clear the contents of the JSON file
    data = {}
    # data = {
    #   "kruh za dopeko": {
    #     "\"BAGETA S ČESNOM IN MASLOM SPAR, 175G\"": "4",
    #     "\"KAJZERICE ZA DOPEKO, S-BUDGET, 6/1, 420G\"": "2",
    #     "\"BIO PŠENIČNO PEKOVSKO PECIVO ZA DOPEKO, SPAR NATUR*PUR, 4/1, 250G\"": "2",
    #     "KRUH ZA DOPEKO": "4"
    #   }
    # }

    with open(f'./temp_repo/{file_path}', 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file)

    # Add monthly shopping list to the staging area
    repo.index.add(['monthly-shopping-list.json'])

    # Commit the changes
    repo.index.commit(commit_message)

    # Push the changes back to the remote repository
    origin = repo.remote('origin')
    try:
        origin.push()
        print("Changes pushed successfully.")

        # delete the local repo after pushing .temp_repo
        repo.git.clear_cache()
        repo.close()
        # remove the temp_repo folder and .git folder
        folder_path = 'temp_repo/.git'
        folder_root = 'temp_repo'

        if platform == "win32":
            os.system('rd /s /q "{}"'.format(folder_path))
            os.system('rd /s /q "{}"'.format(folder_root))

        # TODO test if works for linux too
        elif platform == "linux" or platform == "linux2":
            os.system('rm -rf ' + folder_path)
            os.system('rm -rf ' + folder_root)
        else:
            raise Exception("Not Windows or Linux detected: '%s'" % platform)

    except GitCommandError as error:
        print(f"Error pushing to remote: {error}")


change_git_file(repo_url, file_path, commit_message)

"""
{
  "kruh za dopeko": {
    "\"BAGETA S ČESNOM IN MASLOM SPAR, 175G\"": "4",
    "\"KAJZERICE ZA DOPEKO, S-BUDGET, 6/1, 420G\"": "2",
    "\"BIO PŠENIČNO PEKOVSKO PECIVO ZA DOPEKO, SPAR NATUR*PUR, 4/1, 250G\"": "2",
    "KRUH ZA DOPEKO": "4"
  }
}
"""