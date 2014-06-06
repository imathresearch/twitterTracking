from TwitterTracking.core.kernel.twitterTrack import TwitterTracker
from SentimentAnalysis.core.kernel.analysisNB import NbAnalyzer
import json
import os

os.environ["COLLECTION_NAME"] = 'twitter_tracker'
fileName = 'partialData.txt'


l_query = ['spain']
timeout = 5

tt = TwitterTracker(l_query, timeout, fileName)


split_query = l_query[0].split(',');

sentiment_dictionary = {};

for t in split_query:
    print "here 1"
    list_tweets = tt.getTweets_ByTrackKey(t);
    print "here 2"
    text_tweets = [w['text'] for w in list_tweets]
    print "here 3"
    nb_classiffier = NbAnalyzer();
    sentiment_list = nb_classiffier.predict(text_tweets);
    print "here 4"
    sentiment_dictionary[t] = sentiment_list;

print sentiment_dictionary

print json.dumps(sentiment_dictionary)
