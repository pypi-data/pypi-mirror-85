import asyncio
from pit2ya.db import get_data, set_data
from pit2ya.toggl_wrap import begin_timer_raw

def user_start():
    from iterfzf import iterfzf
    desc_list = get_data()
    query, desc = iterfzf(desc_list, print_query=True, extended=True)
    if desc:
        begin_timer_raw(desc, desc_list.timers[desc]['pid'])
    else:
        pass    # TODO: collect project information, allow creating new time entries
    # set_data(desc_list, desc)  # TODO: put in

def user_modify():
    from iterfzf import iterfzf
    desc_list = get_data()
    # for i,e in enumerate(desc_list):
    #     if i > 20:
    #         break
    query, desc = iterfzf(desc_list, print_query=True, extended=True)
    from toggl.api import TimeEntry
    cur = TimeEntry.objects.current()
    if cur is None:
        print('No current running timer! starting a new one..')
        begin_timer_raw(desc, desc_list.timers[desc]['pid'])
    elif desc:
        setattr(cur, 'description', desc)
        setattr(cur, 'project', desc_list.timers[desc]['pid'])
        cur.save()
    else:       # create a whole new timer
        desc_list.timers[query] = desc_list.timers[desc]
        desc = query
        setattr(cur, 'description', desc)
        cur.save()
    set_data(desc_list, desc)

