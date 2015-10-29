from twython import Twython
from secret import consumer_key, consumer_secret, access_token, access_secret
import requests
import json
import datetime

twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

payload = {
	"userid" : "TwitterBot",
	"device" : "TwitterBot"
}

r = requests.post("http://eventsatnjit.jayravaliya.com/api/v0.2/events", json=payload).json()

currenttime = datetime.datetime.now()

if(currenttime.hour == 9):
	total = 0
	for elem in r["response"]:
		if elem["datetime"]["is_today"] == True:
			total = total + 1

	twitter.update_status(status="TEST - There are " + str(total) + " events taking place today! via @EventsAtNJIT.")

