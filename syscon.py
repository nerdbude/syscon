import os
import shutil
import subprocess
import configparser
import sys

version = "0.1-alpha"

# -----------------------------------------------------
# Lädt die Konfigurationsdatei 'config.ini' mit configparser
# -----------------------------------------------------
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

# -----------------------------------------------------
# Klont das Dotfile-Repository aus der config in den Zielpfad
# -----------------------------------------------------
def git_clone(dotfile_repo, dotfile_path):
	print(':: SYSC0N (' + version + ')')
    print(f":: cloning repo {dotfile_repo} into {dotfile_path}")
    subprocess.run(["git", "clone", dotfile_repo, dotfile_path], check=True)

# -----------------------------------------------------
# Verschiebt den gesamten Inhalt des .config-Verzeichnisses
# in einen Unterordner '.config/old_dots' zur Sicherung
# -----------------------------------------------------
def move_old_config():
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config")
    old_dots_dir = os.path.join(config_dir, "old_dots")
    
    if not os.path.exists(old_dots_dir):
        os.makedirs(old_dots_dir)

    for item in os.listdir(config_dir):
        # Überspringt den Ordner 'old_dots' selbst
        if item == "old_dots":
            continue

        source = os.path.join(config_dir, item)
        destination = os.path.join(old_dots_dir, item)
        shutil.move(source, destination)
	print(':: SYSC0N (' + version + ')')
    print(f":: move old dots to {old_dots_dir}")

# -----------------------------------------------------
# Erstellt symbolische Links von allen Unterordnern im
# Dotfile-Verzeichnis in das .config-Verzeichnis
# -----------------------------------------------------
def create_symlinks(dotfile_path):
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config")

    for subdir in os.listdir(dotfile_path):
        subdir_path = os.path.join(dotfile_path, subdir)
        link_path = os.path.join(config_dir, subdir)

        # Nur für Verzeichnisse symbolische Links erstellen
        if os.path.isdir(subdir_path):
            # Falls ein Link oder Ordner schon existiert, löschen
            if os.path.exists(link_path) or os.path.islink(link_path):
                os.remove(link_path)
            os.symlink(subdir_path, link_path)
            print(f":: linking {link_path} -> {subdir_path}")

# -----------------------------------------------------
# Führt git add, commit und push aus, um Änderungen hochzuladen
# -----------------------------------------------------
def push_changes():
	print(':: SYSC0N (' + version + ')')
    print(":: push dots to git ")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Push changes"], check=True)
    subprocess.run(["git", "push"], check=True)

# -----------------------------------------------------
# Holt die neuesten Änderungen aus dem Remote-Repository
# -----------------------------------------------------
def pull_changes():
	print(':: SYSC0N (' + version + ')')
    print(":: pull dots from git ")
    subprocess.run(["git", "pull"], check=True)

# -----------------------------------------------------
# Fügt einen neuen Konfigurationsordner zu den Dotfiles hinzu:
# 1. Fragt Benutzer nach Pfad
# 2. Verschiebt ihn in das Dotfile-Verzeichnis
# 3. Erstellt einen Symlink im .config-Verzeichnis
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
# Hauptfunktion zur Steuerung der Befehle
# -----------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python syscon.py [-init | -push | -pull | -add]")
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
        print("Invalid argument. Use -init, -push, -pull, or -add.")
        sys.exit(1)

# -----------------------------------------------------
# Einstiegspunkt des Skripts
# -----------------------------------------------------
if __name__ == "__main__":
    main()
