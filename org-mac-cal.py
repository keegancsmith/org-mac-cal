#!/usr/bin/env python3

import datetime
import glob
import os.path
import re

from icalendar.cal import Calendar

def glob_contents(pathname):
    for p in glob.iglob(pathname, recursive=True):
        with open(p, encoding='UTF-8') as f:
            yield f.read()

def events(contents):
    for b in contents:
        try:
            cal = Calendar.from_ical(b)
            for c in cal.walk():
                if c.name == 'VEVENT':
                    yield c
        except ValueError:
            pass

disallowed = (
    # ugly zoom link
    'applications.zoom.us',
    # Zoom user link
    'zoom.us/u',
)

# From https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


def main(startFilter=None):
    pattern = os.path.expanduser("~/Library/Calendars/**/*.ics")
    contents = glob_contents(pattern)

    # Default filter is just today
    if startFilter is None:
        today = datetime.date.today()
        startFilter = lambda d: d == today

        # PERF: Only parse contents which include todays date in them. +/- a day
        # to account for timezone differences.
        dateStrs = [datetime.date.fromordinal(today.toordinal() + d).strftime('%Y%m%d') for d in (-1, 0, 1)]
        contents = (b for b in contents if any(sub in b for sub in dateStrs))

    all_events = set()
    for ev in events(contents):
        start = ev.decoded('dtstart')

        # exclude all day events
        if not isinstance(start, datetime.datetime):
            continue

        start = start.astimezone(tz=None)

        if not startFilter(start.date()):
            continue

        end = ev.decoded('dtend').astimezone(tz=None)
        ts = f'<{start:%Y-%m-%d %a %H:%M}-{end:%H:%M}>'

        title = ev.decoded('summary').decode('UTF-8')
        title = deEmojify(title).strip()

        # I get these at a specific time, but I can do them anytime that day.
        if m := re.match(r'^Grade Coding Exercise - ([^-]*) -', title):
            title = f'TODO Grade {m[1]}'
            ts = f'SCHEDULED: <{start:%Y-%m-%d %a}>'

        # Remove my name from 1on1 titles
        for s in ('Keegan', '/', '<>'):
            title = title.replace(s, '')
            pass
        title = ' '.join(title.split())

        desc = ''
        if 'description' in ev:
            desc = ev.decoded('description')
            desc = desc.decode('UTF-8')
            links = []
            for link in re.findall(r'https?://[^ \n"<#]+', desc):
                if any(sub in link for sub in disallowed):
                    continue
                if link in links:
                    continue
                links.append(link)
            desc = '\n'.join(links)

        all_events.add((ts, title, desc))

    for ts, title, desc in sorted(all_events):
        print(f'**** {title}')
        print(f'  {ts}')
        if desc:
            print(desc)
        print()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate org from Mac Cal.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--week', action='store_true')
    group.add_argument('--month', action='store_true')
    group.add_argument('--all', action='store_true')

    args = parser.parse_args()

    if args.week:
        today = datetime.date.today()
        monday = today.toordinal() - today.weekday()
        startFilter = lambda d : monday <= d.toordinal() < monday + 7
    elif args.month:
        today = datetime.date.today()
        startFilter = lambda d : d.year == today.year and d.month == today.month
    elif args.all:
        startFilter = lambda d : True
    else:
        # Day is the default
        startFilter = None
    
    main(startFilter)

