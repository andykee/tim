import datetime
import os

import tim


def readfile(file, parser=None):
    if not os.path.exists(file):
        return []
    
    if parser is None:
        parser = tim.core.parser()

    with open(file, 'r') as f:
        data = f.read().strip('\t')
        if data[0:1] != "\n":
            data = "\n" + data

    return [tim.core.Entry(**e) for e in parser.parse(data)]


def writefile(file, entries):
    with open(file, 'w') as f:
        for entry in entries:
            f.write(entry.str)
            f.write('\n')


def duration(start):
    delta = datetime.datetime.now() - start
    hours = delta.days * 24 * 60
    seconds = delta.seconds
    hours += seconds // 3600
    seconds = seconds % 3600
    return hours + seconds / 3600


def running(entries):
    return list(filter(lambda entry: entry.running is True, entries))
