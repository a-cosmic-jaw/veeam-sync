import click
import os
import datetime
import sys

log = None
def tell(msg, error=False):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    if error:
        print(timestamp + " " + msg, file=sys.stderr)
    else:
        print(timestamp + " " + msg)
    log.write(timestamp + " " + msg)

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
        os.makedirs(destination)
        tell("Destination folder created.")

if __name__ == '__main__':
    main()