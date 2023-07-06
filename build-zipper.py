#!/bin/python3
import os
import sys
import zipfile

# This script assumes a directory structure of the following:
# Containing Folder
# - Linux
#   - *Godot Linux Build*
# - Web
#   - *Godot Web Build*
# - Windows
#   - *Godot Windows Build*
# - build-zipper.py

# At least one platform folder (Linux, Web, Windows) must exist.
# If none exist, the script will fail to run.

script_dir: str = os.path.dirname(os.path.realpath(__file__))
web_dir: str = os.path.join(script_dir, "Web")
linux_dir: str = os.path.join(script_dir, "Linux")
windows_dir: str = os.path.join(script_dir, "Windows")
game_name: str = ""
silent_mode: bool = False

# Set silent_mode
if len(sys.argv) > 1:
    silent_arg: str = sys.argv[1].lower()
    silent_mode = silent_arg == "--silent" or silent_arg == "-s"

def exit_prompt():
    """Shows prompt to user to allow them to review output before exiting.
    Very helpful for Windows.
    """

    if silent_mode: return
    input("Press enter to exit...")

def log(msg: str):
    """Prints message if silent_mode is off.
    :param msg: The message to print to output.
    """

    if silent_mode: return
    print(msg)

def create_archive(platform: str, path: str):
    """Creates a zip archive with the proper name formatting.
    :param platform: The name of the platform this zip is for.
    :param files: An array of file paths that go into this zip.
    """

    global game_name
    if not os.path.exists(path): return
    log("Creating "+platform+" archive...")

    files: list[str] = get_files(path)

    os.chdir(path)
    archive_name = "["+platform+"] "+game_name+".zip"
    with zipfile.ZipFile(os.path.join("..", archive_name), "w", zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file)

    log("Finished creating "+platform+" archive!")

def get_files(path: str, root_path: str = None) -> list[str]:
    """Gets a list of all files in a directory, relative to the directory itself.
    :param path: The directory to walk through
    :param root_path: Internal use. Leave blank. Used to keep track of where to start the relative path.
    """

    if root_path == None:
        root_path = path

    files: list[str] = []
    for _, dirnames, filenames in os.walk(path):
        for filename in filenames:
            abs_path = os.path.join(path, filename)
            if os.path.exists(abs_path):
                rel_path = os.path.relpath(abs_path, root_path)
                files.append(rel_path)
        for dirname in dirnames:
            abs_path = os.path.join(path, dirname)
            if os.path.exists(abs_path):
                files.extend(get_files(abs_path, root_path))

    return files

def set_game_name():
    """Sets the global game_name variable by using one of the platform files.
    """

    global game_name
    chosen_dir: str = ""
    extension: str = ""
    if os.path.exists(windows_dir):
        log("Deducing game name from Windows build...")
        chosen_dir = windows_dir
        extension = ".pck"
    elif os.path.exists(linux_dir):
        log("Deducing game name from Linux build...")
        chosen_dir = linux_dir
        extension = ".pck"
    elif os.path.exists(web_dir):
        log("Deducing game name from Web build...")
        chosen_dir = web_dir
        extension = ".png"
    else:
        log("Fatal: No build directories exist! Tried searching for "+windows_dir+", "+linux_dir+", and "+web_dir+", but none were found!")
        exit_prompt()
        exit(66) # Input error

    files: list[str] = os.listdir(chosen_dir)
    for file in files:
        if file.endswith(extension):
            game_name = os.path.splitext(file)[0]
            log("Deduced game name as: "+game_name)
            break
    if game_name == "":
        log("Fatal: Unable to deduce game name! Could not find file with extension "+extension[1:])
        exit_prompt()
        exit(66) # Input error

def rename_web_index():
    """Renames the html file for Web platform to 'index.html'
    """

    global game_name
    if not os.path.exists(web_dir):
        log("No Web build found.")
        return

    index_file: str = os.path.join(web_dir, game_name+".html")
    renamed_index_file: str = os.path.join(web_dir, "index.html")

    if os.path.exists(renamed_index_file):
        log("Already renamed "+game_name+".html to index.html for Web build, skipping...")
        return

    os.rename(index_file, renamed_index_file)
    log("Renamed "+game_name+".html to index.html for Web build")

def remove_console_exe():
    """Removes the Godot console exe from the Windows platform
    """

    global game_name
    if not os.path.exists(windows_dir):
        log("No Windows build found.")
        return

    console_file: str = os.path.join(windows_dir, game_name+".console.exe")
    if not os.path.exists(console_file):
        log("Already removed console exe from Windows build, skipping...")
        return

    os.remove(console_file)
    log("Removed console exe from Windows build")

def create_all_archives():
    """Packages all platforms into their own separate zip folders
    """

    create_archive("Windows", windows_dir)
    create_archive("Linux", linux_dir)
    create_archive("Web", web_dir)

try:
    set_game_name()
    rename_web_index()
    remove_console_exe()
    create_all_archives()
    exit_prompt()
except:
    log("Fatal: An unexpected error occurred!")
    exit_prompt()
    exit(1)
