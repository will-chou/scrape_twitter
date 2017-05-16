import tweepy

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

for i in searchResults:
	print i.user.screen_name
	print i.created_at
	print ''
	print i.text
	print ''