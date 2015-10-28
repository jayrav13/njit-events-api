from twython import Twython
from secret import consumer_key, consumer_secret, access_token, access_secret

twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

twitter.update_status(status='See how easy using Twython is!')
