# By Jay Ravaliya
# Imports
from twython import Twython
from secret import consumer_key, consumer_secret, access_token, access_secret
from model import Posted, db
import requests
import json
import datetime
import random
import math
import sys

# Set up Twitter keys
twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

# Set up payload for analytics.
payload = {
	"userid" : "TwitterBot",
	"device" : "TwitterBot"
}

# Send post request to API to get data, convert it to JSON right away.
r = requests.post("http://eventsatnjit.jayravaliya.com/api/v0.2/events", json=payload).json()

# Retrive current time.
currenttime = datetime.datetime.now()

# Total number of events, counted.
total = 0

# At 8:00 AM, post morning tweet.
if(currenttime.hour == 8):
	# Count total elements that are taking place today. Post it.
	# Else, post that there are no events going on.
	for elem in r["response"]:
		if elem["datetime"]["is_today"] == True:
			total = total + 1

	if total > 0:
		tweet = "There are " + str(total) + " events taking place today! Be sure to stop by and check some out! via @EventsAtNJIT"
	else:
		tweet = "Ah - no events going on today! Be sure to check back tomorrow to see what's going on!"

	print(tweet)
	twitter.update_status(status=tweet)

# If posting at night, post # of events going on tomorrow.
elif(currenttime.hour == 22):
	tweet = "That's all for today! Visit back tomorrow to learn about the awesome events taking place on campus! via @EventsAtNJIT"	
	twitter.update_status(status=tweet)

# Posting every two hours:
else:
	# Starting text.
	starters = [
		"Awesome event coming up: ",
		"Did you know? ",
		"Check this out: ",
		"Stop by: "
	]

	# Categories to include.
	categories = [
		"Intramurals & Recreation",
		"Reception, Banquet, Party",
		"Lecture, Seminar, Workshop",
		"Conference, Fair",
		"Other"
	]

	# Count the number of events. Exit if there are no events left.
	num_events = 0

	def today_events():
		global num_events
		for elem in r["response"]:
			if (elem["datetime"]["is_today"] == True or elem["datetime"]["is_tomorrow"]):
				num_events = num_events + 1

	today_events()
	
	if (num_events == 0):
		print "NO EVENTS"
		sys.exit()

	# Input JSON element - ouput validity.
	def valid_event(elem):
		if (elem["datetime"]["is_today"] == True or elem["datetime"]["is_tomorrow"] == True):
			if (elem["datetime"]["multiday"] == False and (elem["datetime"]["currently_happening"] == False or elem["datetime"]["starting_now"] == True)):
				return True
		return False 

	# Input JSON element - output tweet.
	def generate_tweet(elem):
		print("Element Id: " + str(elem["id"]))
		# Random intro, unless happening now.
		if elem["datetime"]["currently_happening"] == True:
			intro = "Happening Now: "
		else:
			intro = starters[int(math.floor(random.random() * len(starters)))]
		
		# Add basic data.
		tweet = "\"" + elem["name"] + "\"" + " hosted by " + elem["organization"] + " "
		if elem["datetime"]["is_today"] == True:
			tweet = tweet + "starts today "
		elif elem["datetime"]["is_tomorrow"] == True:
			tweet = tweet + "starts tomorrow "
		elif elem["datetime"]["currently_happening"] == True:
			tweet = tweet + "started "
		else:
			tweet = tweet + "starts on " + elem["datetime"]["start"]["common_formats"]["date"] + " "

		# Finalize tweet, return.
		tweet = tweet + "at " + elem["datetime"]["start"]["common_formats"]["time"] + " in " + elem["location"] + "."
		if len(intro + tweet) <= 140:
			return intro + tweet
		elif len(tweet) <= 140:
			return tweet
		else:
			return None

	# Loop through events, tweet!
	for elem in r["response"]:
		if valid_event(elem) == True:
			try:
				tweet = generate_tweet(elem) 
				p = Posted.query.filter_by(event_id=elem["id"]).first()
				if tweet != None and p == None:
					print tweet + " / " + str(len(tweet))
					p = Posted(elem["id"])
					db.session.add(p)
					db.session.commit()
					twitter.update_status(status=tweet)
					break
			except:
				pass
