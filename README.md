# org-mac-cal

Generate Emacs org-mode agenda from the calendars synced with Mac Calendar.

## Status

Brand new code. Contains hardcoding of my name/etc. Will likely evolve this
code as I integrate it into my workflow and find the things I wanna change.

Currently excludes recurring events! Will hack on that next time.

## Motivation

This was created to take my current day and generate org entries to show up in my agenda. Additionally it would massage the events into what I care about:

- Only include URLs from description.
- Remove my name from titles (common in 1on1 events, currently hardcoded).
- Remove emoji from titles.
- Dissallow certain URLs (zoom user links, zoom links via google integration).
- Deduplicate events across calendars.
- Events from lever to grade assignments become TODOs on a day, rather than an
  event at a specific time.

## Installation

``` shell
python3 -m venv venv
./venv/bin/pip3 install -r requirements.txt
./venv/bin/python3 org-mac-cal.py
```

## Example

An example from this week with all private info manually redacted.

``` shellsession
$ ./venv/bin/python3 org-mac-cal.py --week
**** Loïc
  <2020-10-26 Mon 16:30-17:00>
https://zoom.us/j/REDACTED

**** Company meeting
  <2020-10-26 Mon 17:00-17:30>
https://zoom.us/j/REDACTED

**** Search sync
  <2020-10-26 Mon 17:30-18:00>
https://docs.google.com/document/d/REDACTED
https://zoom.us/j/REDACTED

**** TODO Grade REDACTED
  SCHEDULED: <2020-10-27 Tue>
https://hire.lever.co/interviews/REDACTED

**** Hack Hour Tomás
  <2020-10-28 Wed 14:30-15:20>
https://zoom.us/j/REDACTED

**** 31337 h4cking: Thorsten
  <2020-10-28 Wed 16:15-17:00>
https://zoom.us/j/REDACTED

**** Erik Hack
  <2020-10-29 Thu 14:00-15:00>
https://zoom.us/j/REDACTED

**** Loïc Hack
  <2020-10-29 Thu 15:00-15:50>

**** Search team halloween
  <2020-10-30 Fri 17:00-17:50>
https://zoom.us/j/REDACTED
```
