from pit2ya.toggl_wrap import get_timers
from os import getenv, path, replace
from csv import reader, writer
from itertools import chain

filepath = getenv('PIT2YA_DIRPATH') or getenv('XDG_DATA_HOME') + '/pit2ya/timers.csv'
dirpath = filepath[:filepath.rfind('/')]

def api_and_yield(path, days, timers):
    for timer in get_timers(days):
        if not timer['desc'] in timers:
            timers[timer['desc']] = { 'pid': timer['pid'] }
            yield timer['desc']

class get_data():   # https://stackoverflow.com/q/34073370
    def __init__(self):
        self.timers = {}
        self.reader = None
        if path.isfile(filepath):
            # with open(filepath, 'r', newline='') as rof:
            self.file_handle = open(filepath, 'r', newline='')
            self.reader = reader(self.file_handle) # TODO: yes memory leak, too bad (how to lifetimes?)
            self.recent_gen = api_and_yield(filepath, 1, self.timers)
        else:
            if not path.isdir(dirpath):
                from os import mkdir
                mkdir(dirpath)
            print('cached data file not found... loading past toggl data')
            self.recent_gen = api_and_yield(filepath, 30, self.timers)
    def __iter__(self):
        return self
    def __next__(self):
        if self.reader:
            try:
                row = next(self.reader)
                self.timers[row[0]] = { 'pid': int(row[1] or -1) }
                return row[0]
            except StopIteration:
                self.file_handle.close()
                self.reader = None
                return next(self.recent_gen)
        else: # can't just else because it might have changed
            return next(self.recent_gen)

def set_data(desc_list, recent):
    with open(filepath + '.bak', 'w+', newline='') as wof:    # TODO: delete the line instead of rewriting. or use an actual database
        wf = writer(wof)
        wf.writerow([recent, desc_list.timers[recent]['pid']])
        for timer_k in chain(desc_list.timers, desc_list):
            if timer_k is not recent:
                wf.writerow([timer_k, desc_list.timers[timer_k]['pid']])
    replace(filepath + '.bak', filepath)

