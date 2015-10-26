# imports
import requests
from lxml import html
from model import db, Events
import urllib2

# arr is for event data to be stored, recording is a flag to determine when to commit data to the database.

options = ["X-TRUMBA-CUSTOMFIELD;NAME=\"Event Name\";ID=6143;TYPE=SingleLine", "SUMMARY", "LOCATION", "DTSTART;TZID=America/New_York", "DTEND;TZID=America/New_York", "X-MICROSOFT-CDO-ALLDAYEVENT", "X-TRUMBA-CUSTOMFIELD;NAME=\"Organization\";ID=5323;TYPE=SingleLine", "DESCRIPTION", "CATEGORIES"]
recording = False

# Clear all events from the database
Events.query.delete()

# pull all events from .ics file
events = urllib2.urlopen("http://25livepub.collegenet.com/calendars/NJIT_EVENTS.ics")

# clean up events text file
def parse_events(events):
	total = ""
	arr = []
	for line in events:
		if line[0] == " ":
			edited = line[1:].replace("\\", "").rstrip("\r\n")
			total = total + edited
		else:
			arr.append(total)
			total = line.rstrip("\r\n")
	
	return arr

events = parse_events(events)

# loop through each line
for line in events:
	
	# split each line by the first ":" mark.
	sections = line.split(":", 1)
	# if this is the beginning of an event, reset array and indicate that the data should start recording
	if "BEGIN" in sections[0] and "VEVENT" in sections[1]:
		arr = [None, None, None, None, None, None, None, None, None]
		recording = True

	# if this is the end of an event, create an event object and add it to the database. end recording.
	if "END" in sections[0] and "VEVENT" in sections[1]:	
		event = Events(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8])
		db.session.add(event)
		recording = False

	# if currently recording and the section header is one of the required, add it to the array.
	# be sure to replace all end characters and decode utf8 for strange characters.
	if recording and sections[0] in options:	
		arr[options.index(sections[0])] = sections[1].replace("\r\n", "").replace("\\", "").decode('UTF8')

# Commit everything to a database
db.session.commit()
print "Successfully executed scrape.py for the \"Events at NJIT\" app."
