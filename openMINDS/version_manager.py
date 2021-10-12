import os
import git
import json
import click

from pathlib import Path

REPO_URL = "https://github.com/HumanBrainProject/openMINDS/"
DEFAULT_DIRECTORY = ".openMINDS"
CONFIG_FILE = os.path.join(Path.home(), ".openMINDS.conf")
VERSION_DESCRIPTIONS = "./version_descriptions.json"

#target_directory = os.path.join(Path.home(), DEFAULT_DIRECTORY)

class MyProgressPrinter(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

        
def _get_version_descriptions():
    with open(VERSION_DESCRIPTIONS, "r") as f:
        return json.load(f)

    
def _get_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

    
def _update_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

            
def update_openMINDS(target_directory=None):
    if target_directory is None:
        target_directory = os.path.join(Path.home(), DEFAULT_DIRECTORY)
    
    if os.path.exists(target_directory):
        print("openMINDS directory exists")
        print("Checking for updates")
        repo = git.Repo(target_directory)
        origin = repo.remotes[0]
        origin.pull()
    else:
        print("Target directory will created")
        print("Cloning openMINDS to target directory")
        repo = git.Repo.clone_from(REPO_URL, target_directory, branch='documentation')

        
def version_selection(selected_version):
    if check_valid_version(selected_version):
        config = _get_config()
        config["selected_version"] = selected_version
        _update_config(config)


def get_available_versions():
    config = _get_config()
    
    target_content = os.listdir(config["openMINDS_directory"])
    versions = []
    
    ignored_elem = [".git"]
    
    for elem in target_content:
        if os.path.isdir(config["openMINDS_directory"] + "/" + elem) and elem not in ignored_elem:
            versions.append(elem)

    return versions

    
def check_valid_version(v):
    return v in get_available_versions()


@click.group()
def version_manager_cli():
    pass


@click.command()
def select_version():
    print("Available versions:")
    print("")
    
    index = 1

    version_descriptions = _get_version_descriptions()
    
    for version in get_available_versions():
        try:
            description = version_descriptions["versions"][version]
        except:
            print("Version without description")
            
        print("\t" + str(index) +"\t" + version + "\t"  + description)
        index += 1
        
    print("")
    print("Select version to use:")
    selection = input()
    
    try:
        selected_version = get_available_versions()[int(selection) - 1]
        print("Selected version: " + selected_version)
    except:
        print("Invalid input")

    version_selection(selected_version)

def init(target_dir=None):
    if target_dir is None:
        target_dir = os.path.join(Path.home(), DEFAULT_DIRECTORY)
        
    update_openMINDS(target_dir)

    config = {
        "openMINDS_directory": target_dir,
        "selected_version": None
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
        

@click.command()
@click.option("--target_dir", default=os.path.join(Path.home(), DEFAULT_DIRECTORY), help="Destination directory for downloaded openMINDS.\nDefault is .openMINDS in the user home-directory.")
def init_repo(target_dir):
    init(target_dir)
        

@click.command()
def update_repo():
    config = _get_config()
    update_openMINDS(config["openMINDS_directory"])

    
@click.command()
def status():
    config = _get_config()

    print("")
    print("Current openMINDS configuration")
    print("")
    
    if config["selected_version"] is None:
        print ("Selected version:\tCurrently no version selected")
    else:
        print("Selected version:\t" + config["selected_version"])
    print("openMINDS directory:\t" + config["openMINDS_directory"])
    print("")
    
    
version_manager_cli.add_command(init_repo)
version_manager_cli.add_command(update_repo)
version_manager_cli.add_command(select_version)
version_manager_cli.add_command(status)

if __name__ == '__main__':
    version_manager_cli()
