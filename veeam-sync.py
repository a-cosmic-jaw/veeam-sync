import click

@click.command()
@click.option('--logfile', type=str, required=True)
@click.option('--source', type=str, required=True)
@click.option('--destination', type=str, required=True)
def start():
    pass

if __name__ == '__main__':
    start()