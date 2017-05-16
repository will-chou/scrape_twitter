import tweepy
from pymongo import MongoClient

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
		print i.user.screen_name
		print i.created_at
		print ''
		print i.text
		print ''
		result = db.tweets.insert_one({"Screen name" : i.user.screen_name, "Time/Date" : i.created_at, "Tweet" : i.text})

	#return database object
	return db;

def main():
	db = loadMongoDB(searchTweets())

if __name__ == "__main__":
	main()
