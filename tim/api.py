from datetime import datetime

import click

from tim.db import create_engine, create_session
from tim.models import Base, Entry
from tim.queries import open_entries


DB = create_engine()
Base.metadata.create_all(DB)


@click.group()
def tim():
    pass


@tim.command()
@click.argument('note', nargs=1, required=False)
@click.option('--tag', '-t', multiple=True)
def start(note, tag):
    

    with create_session(DB).begin() as session:
        session.add(Entry(start=datetime.now(),
                          note=note))


@tim.command()
@click.argument('id', nargs=1, required=False)
def stop(id):
    with create_session(DB).begin() as session:
        entries = open_entries(session)

        match len(entries):
            case 0:
                print('nope')
            case 1:
                entries[0].stop = datetime.now()
            case _:
                if id:
                    entry = _id_entry(id, entries)
                    entry.stop = datetime.now()
                else:
                    _print_open_entries(entries)


@tim.command()
def status():
    _status()


@tim.command()
def st():
    _status()


@tim.command()
@click.option('--number', '-n', type=int, default=10)
@click.option('--tag', '-t', multiple=True)
def log(number):
    pass


@tim.command()
def report():
    pass


def _status():
    with create_session(DB).begin() as session:
        entries = open_entries(session)
        _print_open_entries(entries)


def _id_entry(id, entries):

    id = int(id.strip('@'))
    index = [len(entries)-n for n in range(len(entries))].index(id)
    return entries[index]


NOTE_LEN = 45

def _print_open_entries(entries):

    header = 'id'.ljust(4) + 'start time'.ljust(21) + 'note'
    click.echo(header)
    click.echo('-' * 79)

    nentries = len(entries)

    for n, entry in enumerate(entries):
        start_time = entry.start.strftime('%Y-%m-%d %H:%M:%S')
        
        note = '' if entry.note is None else entry.note

        if len(note) > NOTE_LEN:
            note = note[:NOTE_LEN - 3] + '...'

        click.secho(f'@{len(entries) - n:<3}', fg='yellow', nl=False)
        click.echo(f'{start_time:<21}{note:<45}')
    


