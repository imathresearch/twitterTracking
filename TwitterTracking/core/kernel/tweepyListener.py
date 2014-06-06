from TwitterTracking.core.constants import CONS
import tweepy
from tweepy.api import API
from tweepy.utils import import_simplejson
import time
from TwitterTracking.core.util.tweetUtils import TweetUtils
from multiprocessing import JoinableQueue

tweetUtils = TweetUtils()

json = import_simplejson()
C = CONS()

class Listener(tweepy.StreamListener):

    def __init__(self, tweet_queue, timeout, api=None):
        self.api = api or API()
        self.tweet_queue = tweet_queue
        self.timeout = timeout
        self.init_time = time.time()


    def on_data(self, tweet):
        decoded_tweet = json.loads(tweet)
        self.tweet_queue.put(decoded_tweet['text'])
                
        current_time = time.time()
        if current_time - self.init_time > self.timeout:
            self.tweet_queue.put(C.TOKEN_LAST_TWEET)
            return False
        else:
            return True

    
    def on_error(self, status):
        return False

    def on_timeout(self, timeout):
        return False