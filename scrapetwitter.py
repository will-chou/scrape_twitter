import tweepy
from random import randint
from pymongo import MongoClient
from twilio.rest import Client

#function that searches for tweets matching query string and stores them into a list of SearchResult objects
def searchTweets():
	#consumer key and secret obtained from Twitter Developer Account
	CONSUMER_KEY = 'tEgCRfWRBzj7hiV76oiw9mZNO'
	CONSUMER_SECRET = 'gO6bEoCmZH3D418A27PLizmzqd0IBS0huQ0SQLGEZTjKi1mXy3'

	#access token and secret obtained from Twitter Developer Account
	ACCESS_TOKEN = '863661949665419264-g27TkFv7Z4XBZ8JfkZ9ZGV7gzthMzSO'
	ACCESS_TOKEN_SECRET = 'Du0U7SwMlDv13QaKBjHw68fkUWoyjtbn713Cp2TCQYeHH'

	#consumer and access info needed to authenticate Python application with Twitter using Tweepy
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth)

	#searches for tweets matching query string "going for a run", stores 'count' results into list
	search_results = api.search(q="\"going for a run\"", count=100)

	#return the saved search results
	return search_results

#function that loads search results into a MongoDB database
def loadMongoDB(searchResults):
	#connect to mongo instance via MongoClient
	client = MongoClient();

	#create database
	db = client.tweetdb

	#clear tweets collection before loading tweets in
	db.tweets.delete_many({})

	#iterate through search results list, insert tweets with their respective usernames and time/dates
	for i in searchResults:
		result = db.tweets.insert_one({"Screen name" : i.user.screen_name, "Time/Date" : i.created_at, "Tweet" : i.text})

	#return database object
	return db;

#function that sends SMS through integration with Twilio
def sendSMS(db):
	#generate random number that corresponds to random tweet
	rand = randint(0, 99)

	#find the random tweet
	tw = db.tweets.find(skip=rand, limit=1)[0]

	#generate formatted string of the tweet that is to be sent
	tweetstring = "Username: " + tw["Screen name"] + "\nDate/Time: " + tw["Time/Date"].strftime("%b %d %Y\t%X") + "\nTweet: " + tw["Tweet"]
	print(tweetstring)

	#obtain account_sid and auth_token from Twilio Account
	account_sid = "ACa1de66ad7121e0a97564a15bbd416d68"
	auth_token = "0b4b216f5ce14dda98693d1f43f19913"

	#connect to Twilio
	client = Client(account_sid, auth_token)

	#generate text message with formatted tweet string and send via SMS to phone number
	client.messages.create(to="+19786186820", from_="+16692717473", body=tweetstring)

def main():
	db = loadMongoDB(searchTweets())
	sendSMS(db)

if __name__ == "__main__":
	main()
