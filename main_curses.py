#!/usr/bin/python

import sys
from GCalendar import *
import curses

stdscr = curses.initscr()


def start_curses():
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)


def end_curses():
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


def draw_with_calendar_list(screen, calendar_list):
    y = 0
    for calendar_data in calendar_list:
        screen.addstr(y, 0, calendar_data.summary)
        y += 1
        for event in calendar_data.events:
            screen.addstr(y, 1, event.summary)
    screen.refresh()


if __name__ == '__main__':

    # we're going to want to delay starting curses until after we auth!
    # move to after teh ctor for GCalendar
    start_curses()
    calendar = GCalendar('client_secrets.json', sys.argv)
    stdscr.nodelay(1)

    calendar_list = calendar.get_calendar_list()

    while 1:
        c = stdscr.getch()
        if c == ord('q'):
            break
        draw_with_calendar_list(stdscr, calendar_list)

    end_curses()
