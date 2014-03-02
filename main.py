#!/usr/bin/python

import sys
from GCalendar import *

if __name__ == '__main__':
    calendar = GCalendar('client_secrets.json', sys.argv)
    for calendar_data in calendar.get_calendar_list():
        print calendar_data.summary
