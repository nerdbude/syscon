import os
import shutil
import subprocess
import configparser
import sys

version = "0.1-alpha"

# -----------------------------------------------------
# Load config.ini 
# -----------------------------------------------------
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

# -----------------------------------------------------
# clone dotfile-repo from config
# -----------------------------------------------------
def git_clone(dotfile_repo, dotfile_path):
    print(':: SYSC0N (' + version + ')')
    print(f":: cloning repo {dotfile_repo} into {dotfile_path}")
    subprocess.run(["git", "clone", dotfile_repo, dotfile_path], check=True)

# -----------------------------------------------------
# make backup from old dots
# -----------------------------------------------------
def move_old_config():
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config")
    old_dots_dir = os.path.join(config_dir, "old_dots")
    
    if not os.path.exists(old_dots_dir):
        os.makedirs(old_dots_dir)

    for item in os.listdir(config_dir):
        # ignore 'old_dots'
        if item == "old_dots":
            continue

        source = os.path.join(config_dir, item)
        destination = os.path.join(old_dots_dir, item)
        shutil.move(source, destination)
    print(':: SYSC0N (' + version + ')')
    print(f":: move old dots to {old_dots_dir}")

# -----------------------------------------------------
# create symlinks from dots to /.config
# -----------------------------------------------------
def create_symlinks(dotfile_path):
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config")

    for subdir in os.listdir(dotfile_path):
        subdir_path = os.path.join(dotfile_path, subdir)
        link_path = os.path.join(config_dir, subdir)

        # symlinks for folders
        if os.path.isdir(subdir_path):
            # del if exist
            if os.path.exists(link_path) or os.path.islink(link_path):
                os.remove(link_path)
            os.symlink(subdir_path, link_path)
            print(f":: linking {link_path} -> {subdir_path}")

# -----------------------------------------------------
# git add, commit and push
# -----------------------------------------------------
#def push_changes():
#    print(':: SYSC0N (' + version + ')')
#    print(':: push dots to git ')
#    subprocess.run(["git", "add", "."], check=True)
#    subprocess.run(["git", "commit", "-m", "Push changes"], check=True)
#    subprocess.run(["git", "push"], check=True)
def push_changes():
    print(':: SYSC0N (' + version + ')')
    print(':: push dots to git ')

    # Wechsel in das Root-Verzeichnis des Repositories
    repo_dir = os.path.abspath('.')  # Stelle sicher, dass du im richtigen Repo-Verzeichnis bist
    if not os.path.exists(os.path.join(repo_dir, ".git")):
        print(f"Fehler: Das Verzeichnis {repo_dir} scheint kein Git-Repository zu sein.")
        return

    # Überprüfe den git-Status, bevor du mit dem Commit fortfährst
    result = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=repo_dir)
    if result.returncode != 0:
        print(f"Fehler bei git status: {result.stderr.decode()}")
        return

    status_output = result.stdout.decode()
    if not status_output.strip():
        print(":: Keine Änderungen zu committen.")
        return

    # Führe Git-Befehle im richtigen Arbeitsverzeichnis aus
    subprocess.run(["git", "add", "."], check=True, cwd=repo_dir)
    subprocess.run(["git", "commit", "-m", "Push changes"], check=True, cwd=repo_dir)
    subprocess.run(["git", "push"], check=True, cwd=repo_dir)

# -----------------------------------------------------
# git pull
# -----------------------------------------------------
def pull_changes():
    print(':: SYSC0N (' + version + ')')
    print(':: pull dots from git ')
    subprocess.run(["git", "pull"], check=True)

# -----------------------------------------------------
# ask for path to new dotfiles
# -----------------------------------------------------
def add_dotfile():
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config")
    dotfile_path = load_config().get('Settings', 'dotfile_path')
    print(':: SYSC0N (' + version + ')')
    folder_path = input(":: path to dotfile: ").strip()

    if not os.path.exists(folder_path):
        print(f":: '{folder_path}' does not exist.")
        return

    folder_name = os.path.basename(folder_path)
    destination = os.path.join(dotfile_path, folder_name)

    if os.path.exists(destination):
        print(f":: folder '{folder_name}' already exists in {dotfile_path} ")
    else:
        shutil.move(folder_path, destination)
        print(f"Moved {folder_path} to {dotfile_path}.")

    link_path = os.path.join(config_dir, folder_name)

    if os.path.exists(link_path) or os.path.islink(link_path):
        os.remove(link_path)
    os.symlink(destination, link_path)
    print(f":: created symlink: {link_path} -> {destination}")

# -----------------------------------------------------
# commands
# -----------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print('Usage: python syscon.py [-init | -push | -pull | -add]')
        sys.exit(1)

    config = load_config()
    machine_name = config.get('Settings', 'machine_name')
    dotfile_repo = config.get('Settings', 'dotfile_repo')
    dotfile_path = config.get('Settings', 'dotfile_path')

    if sys.argv[1] == "-init":
        git_clone(dotfile_repo, dotfile_path)
        move_old_config()
        create_symlinks(dotfile_path)

    elif sys.argv[1] == "-push":
        push_changes()

    elif sys.argv[1] == "-pull":
        pull_changes()

    elif sys.argv[1] == "-add":
        add_dotfile()

    else:
        print('Invalid argument. Use -init, -push, -pull, or -add.')
        sys.exit(1)

# -----------------------------------------------------
# entrypoint 
# -----------------------------------------------------
if __name__ == "__main__":
    main()
