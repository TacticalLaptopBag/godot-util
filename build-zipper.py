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

"""Shows prompt to user to allow them to review output before exiting.
Very helpful for Windows.
"""
def exit_prompt():
    if silent_mode: return
    input("Press enter to exit...")

"""Prints message if silent_mode is off.
:param msg: The message to print to output.
"""
def log(msg: str):
    if silent_mode: return
    print(msg)

"""Creates a zip archive with the proper name formatting.
:param platform: The name of the platform this zip is for.
:param files: An array of file paths that go into this zip.
"""
# TODO: Figure out typing for Array
def create_archive(platform: str, files: Array[str]):
    with zipfile.ZipFile("["+platform+"] "+game_name+".zip", "w", ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file)

"""Sets the global game_name variable by using one of the platform files.
"""
def set_game_name():
    global game_name
    chosen_dir: str = ""
    extension: str = ""
    if os.path.exists(windows_dir):
        log("Deducing game name from Windows build...")
        chosen_dir = windows_dir
        extension = ".exe"
    elif os.path.exists(linux_dir):
        log("Deducing game name from Linux build...")
        chosen_dir = linux_dir
        extension = ".x86_64"
    elif os.path.exists(web_dir):
        log("Deducing game name from Web build...")
        chosen_dir = web_dir
        extension = ".png"
    else:
        log("Fatal: No build directories exist! Tried searching for "+windows_dir+", "+linux_dir+", and "+web_dir+", but none were found!")
        exit_prompt()
        exit(66) # Input error

    # TODO: Figure out typing for Array
    files: Array[str] = os.listdir(chosen_dir)
    for file in files:
        if file.endswith(extension):
            game_name = os.path.splitext(file)[0]
            log("Deduced game name as: "+game_name)
            break
    if game_name == "":
        log("Fatal: Unable to deduce game name! Could not find file with extension "+extension[1:])
        exit_prompt()
        exit(66) # Input error

"""Renames the html file for Web platform to 'index.html'
"""
def rename_web_index():
    global game_name
    if not os.path.exists(web_dir):
        log("No Web build found.")
        return

    index_file: str = os.path.join(web_dir, game_name+".html")
    renamed_index_file: str = os.path.join(web_dir, "index.html")
    os.rename(index_file, renamed_index_file)
    log("Renamed "+game_name+".html to index.html for Web build")

"""Removes the Godot console exe from the Windows platform
"""
def remove_console_exe():
    global game_name
    if not os.path.exists(windows_dir):
        log("No Windows build found.")
        return

    # TODO: Confirm console file name
    console_file: str = os.path.join(windows_dir, game_name+".console.exe")
    os.remove(console_file)
    log("Removed console exe from Windows build")

"""Packages all platforms into their own separate zip folders
"""
def create_all_archives():
    global game_name
    # TODO
    log("Not implemented yet!")

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
