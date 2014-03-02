
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import httplib2
import os
import sys
import argparse

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
FLOW = client.flow_from_clientsecrets(
	CLIENT_SECRETS,
	scope=['https://www.googleapis.com/auth/calendar.readonly'],
	message=tools.message_if_missing(CLIENT_SECRETS))
parser = argparse.ArgumentParser(
	description=__doc__,
	formatter_class=argparse.RawDescriptionHelpFormatter,
	parents=[tools.argparser])

def listCalendars(service):
	pageToken = None
	while True:
		calendarList = service.calendarList().list(pageToken=pageToken).execute()
		for calendarListEntry in calendarList['items']:
			print calendarListEntry['summary']
		pageToken = calendarList.get('nextPageToken')

def main(argv):
	flags = parser.parse_args(argv[1:])
	storage = file.Storage('calendar.dat')
	credentials = storage.get()
	if credentials is None or credentials.invalid:
		credentials = tools.run_flow(FLOW, storage, flags)

	http = httplib2.Http()
	http = credentials.authorize(http)

	service = discovery.build('calendar', 'v3', http=http)

	try:
		print "Success!"
		listCalendars()
	except client.AccessTokenRefreshError:
		print ("the credentials are revoked or expired, try again!")

if __name__ == '__main__':
	main(sys.argv)
