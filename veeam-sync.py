import click

@click.command()
@click.option('--logfile', type=str, required=True)
@click.option('--source', type=str, required=True)
@click.option('--destination', type=str, required=True)
def start(logfile, source, destination):
    with open(logfile, 'w') as log:
        print("Logfile found and write permission granted.")
        log.write("Logfile found and write permission granted.")

if __name__ == '__main__':
    start()