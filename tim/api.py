import datetime
import os

import click

from tim import core, util

if (TIMFILE := os.environ.get('TIMFILE')) is None:
    TIMFILE = os.path.join(os.path.expanduser('~'), '.tim')


@click.group()
def tim():
    pass


@tim.command()
@click.argument('account', nargs=1, required=True)
@click.option('--note', '-n', multiple=False)
@click.option('--tag', '-t', multiple=True)
def start(account, note, tag):
    entries = util.readfile(TIMFILE)
    entries.append(core.Entry(datetime=datetime.datetime.now(),
                         account=account.split(':'),
                         note=note,
                         tags=tag))
    util.writefile(TIMFILE, entries)


@tim.command()
@click.argument('id', nargs=1, required=False)
def stop(id):
    entries = util.readfile(TIMFILE)
    
    # indices of running entries
    r = [n for n, entry in enumerate(entries) if entry.running is True]
    
    match len(r):
        case 0:
            raise RuntimeError('No active entries')
        case 1:
            n = r[0]
            entries[n].duration = util.duration(entries[n].datetime)
            util.writefile(TIMFILE, entries)
        case _:
            if id:
                id = int(id)
                n = list(reversed(range(1, len(r)+1))).index(id)
                entries[r[n]].duration = util.duration(entries[r[n]].datetime)
                util.writefile(TIMFILE, entries)
            else:
                print_entries(util.running(entries))


@tim.command()
def status():
    entries = util.readfile(TIMFILE)
    print_entries(util.running(entries))

@tim.command()
def st():
    entries = util.readfile(TIMFILE)
    print_entries(util.running(entries))


def print_entries(entries, note_len=40):

    entry_str = []
    max_account = 7 # account

    for n, entry in enumerate(entries):

        id = len(entries) - n
        start = entry.datetime.strftime('%Y-%m-%d %H:%M:%S')

        account = entry.account_str()
        if len(account) > max_account:
            max_account = len(account)

        dur = util.duration(entry.datetime)
        h = int(dur//1)
        m = round(dur%1 * 60)
        if h == 0:
            duration = f'{m}m'
        else:
                duration = f'{h}h{m}m'

        entry_str.append((id, start, account, duration))
        
    max_account += 2
    header = 'id'.ljust(4) + 'start'.ljust(21) + 'account'.ljust(max_account) + 'duration'
    click.echo(header)
    click.echo('-' * (4+21+max_account+2+8))

    for entry in entry_str:
        click.secho(f'{entry[0]:<4}', fg='yellow', nl=False)
        click.echo(f'{entry[1]:<21}{entry[2]:<{max_account}}{entry[3]}')


def id_entry(id, entries):
    id = int(id)
    index = [len(entries)-n for n in range(len(entries))].index(id)
    return entries[index]