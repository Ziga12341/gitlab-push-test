import json
from git import Repo, GitCommandError
from sys import platform
import os
# import dotenv that you can load data from .env file
# you need to import python-dotenv package
from dotenv import load_dotenv

# import shutil to remove the temp_repo folder
import shutil
import stat
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
    repo = Repo.clone_from(repo_url, f'{os.getcwd()}/temp_repo')

    # Clear the contents of the JSON file
    data = {}

    # open file in temp_repo folder and write data to it (through current working directory)
    with open(f'{os.getcwd()}/temp_repo/{file_path}', 'w', encoding="utf-8") as json_file:
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
        folder_root = 'temp_repo'
        # remove the read-only flag

        def remove_readonly(func, path, _):
            "Clear the readonly bit and reattempt the removal"
            os.chmod(path, stat.S_IWRITE)
            func(path)

        shutil.rmtree(folder_root, onerror=remove_readonly)

    except GitCommandError as error:
        print(f"Error pushing to remote: {error}")


change_git_file(repo_url, file_path, commit_message)