import datetime
import pathlib

from lark import Lark, Transformer


class Entry:

    def __init__(self, datetime, account, note=None, tags=None, duration=None):
        self.datetime = datetime
        self.account = account
        self.note = None if note is None else note
        self.tags = [] if tags is None else tags
        self.duration = None if duration is None else duration
    
    def __str__(self):
        note = "" if self.note is None else f" \"{self.note}\""
        l1 = f"{self.datetime.strftime('%Y-%m-%dT%H:%M:%S')} *{note} {self.tags_str()}"
        l2 = f"{self.account_str()} {self.duration_str()}"
        return f"{l1}\n  {l2}\n"
    
    @property
    def running(self):
        if self.duration is None:
            return True
        return False
    
    @property
    def str(self):
        return self.__str__()

    def tags_str(self):
        s = ''
        for tag in self.tags:
            s += f'#{tag} '
        return s
    
    def account_str(self):
        s = ''
        for account in self.account:
            s += f"{account}:"
        return s[:-1]

    def duration_str(self):
        if self.running:
            return ''
        else:
            h = int(self.duration//1)
            m = round(self.duration%1 * 60)
            if h == 0:
                return f'{m}m'
            else:
                return f'{h}h{m}m'
            

class EntryTree(Transformer):

    def start(self, n):
        return n[1:]

    def entry(self, n):
        e = {}
        for x in n:
            if isinstance(x, dict):
                e.update(x)
        return e
    
    def datetime(self, n):
        dt_dict = {}
        for x in n:
            dt_dict.update(x)
        
        year = dt_dict['year']
        month = dt_dict['month']
        day = dt_dict['day']
        hour = dt_dict['hour']
        minute = dt_dict['minute']
        second = dt_dict['second'] if 'second' in dt_dict.keys() else 0
        microsecond = int(dt_dict['fractional']) if 'fractional' in dt_dict.keys() else 0
        
        dt = datetime.datetime(year, month, day, hour, minute, second, microsecond)

        return {'datetime': dt}

    def year(self, n):
        return {'year': int(n[0])}
    def month(self, n):
        return {'month': int(n[0])}
    def day(self, n):
        return {'day': int(n[0])}
    def hour(self, n):
        return {'hour': int(n[0])}
    def minute(self, n):
        return {'minute': int(n[0])}
    def second(self, n):
        return {'second': int(n[0])}
    def fractional(self, n):
        return {'fractional': int(n[0])}

    def note(self, n):
        return {'note': str(n[0][1:-1])}
    
    def tags(self, n):
        return {'tags': list(n)}
    def tag(self, n):
        return str(n[0])
    
    def account(self, n):
        accountlist = [str(t) for t in n]
        return {'account': accountlist}
    def subaccount(self, n):
        return str(n[0])

    def duration(self, n):
        return {"duration": sum(n)}
    def duration_hour(self, n):
        return int(n[0])
    def duration_minute(self, n):
        return int(n[0])/60
    

dir = pathlib.Path(__file__).parent.resolve()

def parser():

    with open(dir / 'grammar.lark', 'r') as f:
        grammar = f.read()

    return Lark(grammar, parser='lalr', transformer=EntryTree())