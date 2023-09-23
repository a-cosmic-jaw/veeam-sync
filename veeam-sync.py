import click
import os
import datetime
import sys
from os import walk
from pathlib import Path
import shutil

log = None
def tell(msg, error=False):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    msg = timestamp + " " + msg + "\n"
    if error:
        print(msg, file=sys.stderr)
    else:
        print(msg)
    log.write(msg)

@click.command()
@click.option('--logfile', type=str, required=True)
@click.option('--source', type=str, required=True)
@click.option('--destination', type=str, required=True)
def main(logfile, source, destination):
    global log
    try:
        log = open(logfile, 'w')
        tell("Logfile found and write permission granted.")
    except:
        print("Could not open logfile for writing.", file=sys.stderr)
        exit(2)

    if not os.path.exists(source):
        tell("Source folder does not exist.", error=True)
        exit(1)

    if not os.path.exists(destination):
        try:
            os.makedirs(destination)
            tell("Destination folder created.")
        except:
            tell("Could not create destination directory.", error=True)
            exit(3)

    #f = []
    #for (dirpath, dirnames, filenames) in walk(source):
    #    print(dirpath, dirnames, filenames)
    #    f.extend(filenames)
    #
    #print(f)

    
    result = list(Path(source).rglob("*"))
    source_dirs, source_files = [], []
    for path in result:
        path_str = str(path)
        if os.path.isfile(path_str):
            source_files.append(path_str)
        else:
            source_dirs.append(path_str)
        
    destination_dirs = []
    
    for dir in source_dirs:
        destination_dirs.append(dir.replace(source, destination))

    # Create destination directories
    for dir in destination_dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
    
    for source_file in source_files:
        destination_file = source_file.replace(source, destination)
        if not os.path.exists(destination_file):
            shutil.copy2(source_file, destination_file)
            tell("Copied '" + source_file + "' to '" + destination_file + "'.")

if __name__ == '__main__':
    main()