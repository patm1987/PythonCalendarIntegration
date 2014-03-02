
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import os
import argparse
import httplib2

__author__ = 'Patrick'

class GCalendar:
    def authorize(self, credentials):
        http = httplib2.Http()
        http = credentials.authorize(http)
        self._service = discovery.build('calendar', 'v3', http=http)

    def __init__(self, secrets_filename, args, credentials_filename='calendar.dat'):
        self._parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser]
        )
        self._secrets_filename = os.path.join(os.path.dirname(__file__), secrets_filename)
        self._flow = client.flow_from_clientsecrets(
            self._secrets_filename,
            scope=['https://www.googleapis.com/auth/calendar.readonly'],
            message=tools.message_if_missing(self._secrets_filename)
        )
        self._service = None

        flags = self._parser.parse_args(args[1:])
        storage = file.Storage(credentials_filename)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(self._flow, storage, flags)

        self.authorize(credentials)

    def get_calendar_list(self):
        ret = list()
        page_token = None
        while True:
            calendar_list = self._service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                ret.append(CalendarData(calendar_list_entry))
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return ret

class CalendarData:
    def __init__(self, calendar_entry):
        self.id = calendar_entry['id']
        self.selected = calendar_entry['selected']
        self.summary = calendar_entry['summary']