import click
import os
import datetime

log = None
def tell(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    print(timestamp + " " + msg)
    log.write(timestamp + " " + msg)

@click.command()
@click.option('--logfile', type=str, required=True)
@click.option('--source', type=str, required=True)
@click.option('--destination', type=str, required=True)
def main(logfile, source, destination):
    global log
    log = open(logfile, 'w')
    tell("Logfile found and write permission granted.")

if __name__ == '__main__':
    main()