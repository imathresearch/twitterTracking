from TwitterTracking.core.constants import CONS
import tweepy
import time
from pymongo import MongoClient
from TwitterTracking.core.kernel.tweepyListener import Listener
from TwitterTracking.core.kernel.tweetProcessor import TweetProcessor
from multiprocessing import Process, JoinableQueue
import uuid
import os

STOPPED = 'STOPPED'
INITIATED = 'INITIATED'
FINISHED = 'FINISHED'
ERROR = 'ERROR'

C = CONS()

class TwitterTracker(object):
    
    def __init__(self, l_query, timeout, fileName_partialData):
        self.timeout = timeout
        self.l_query = l_query
        self.collection_name = os.environ["COLLECTION_NAME"] #str(uuid.uuid4())  
        self.file_data = fileName_partialData;
        
        self.status = STOPPED
        
        self.q_tweet = JoinableQueue(maxsize=0)
        self.collection = self.__DBConnection()
        self.__startTracker()
    
    def __DBConnection(self):
        client = MongoClient()
        self.db = client[C.TWITTER_DB]
        return self.db[self.collection_name]   
        
    def __startTracker(self):
        
        process_tweetProcessor = Process(target = self.__runTweetProcessor)
        process_listener = Process(target = self.__runListener)
        
        process_listener.start()
        process_tweetProcessor.start()
        
        self.q_tweet.join()
        
        process_tweetProcessor.join()
        process_listener.join()      
               
        self.status = FINISHED
    
    def __runTweetProcessor(self):
        tweetProcessor = TweetProcessor(self.q_tweet, self.collection, self.l_query, self.file_data)
        tweetProcessor.run()
        
    def __runListener(self):
        auth = tweepy.OAuthHandler(C.CONSUMER_KEY, C.CONSUMER_SECRET)
        auth.set_access_token(C.ACCESS_TOKEN, C.ACCESS_TOKEN_SECRET)        
        listener = Listener(self.q_tweet)
        stream = tweepy.Stream(auth, listener)
        self.status = INITIATED
        start_time = time.time()
        try:
            stream.filter(languages = ['en'], track=self.l_query, async=True)

            pass_time = time.time() - start_time
            while(pass_time < self.timeout):
                time.sleep(self.timeout - pass_time)
                pass_time = time.time() - start_time
                #print "SLEEPING" + str(pass_time)
            
            self.q_tweet.put(C.TOKEN_LAST_TWEET)
            stream.disconnect()
            
        except Exception as e:
            s = str(e)
            self.status = ERROR
            stream.disconnect()
        
            
        
    def getStatus(self):
        return self.status
    
    def getTweets(self):
        if self.status == FINISHED:
            return [t for t in self.collection.find()]
        else:
            return None
        
    def getTweets_ByTrackKey(self, key):
        if self.status == FINISHED:         
            result = self.db.command('text', self.collection_name, search=key)
            return [t['obj'] for t in result['results']]         
        else:
            return None
