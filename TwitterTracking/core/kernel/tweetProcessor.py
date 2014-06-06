from TwitterTracking.core.constants import CONS
from TwitterTracking.core.util.tweetUtils import TweetUtils
from SentimentAnalysis.core.kernel.analysisNB import NbAnalyzer
from multiprocessing import Process, JoinableQueue
from TwitterTracking.core.kernel.dataWriter import PartialDataWriter
tweetUtils = TweetUtils()
C = CONS()

class TweetProcessor(object):
    
    def __init__(self, tweet_queue, tweet_collection, track_query, fileName_partialResult):
        self.tweet_queue = tweet_queue
        self.tweet_collection = tweet_collection
        self.track_query = track_query
        self.nb_classiffier = NbAnalyzer();
        self.file_partialResult = fileName_partialResult;
        self.output_queu = JoinableQueue(maxsize=0)
        
    def run(self):
        process_dataWriter = Process(target = self.__runDataWriter)       
        process_dataWriter.start();
        while True:
            tweet = self.tweet_queue.get()
            if tweet == C.TOKEN_LAST_TWEET:
                self.tweet_queue.task_done()
                #self.tweet_collection.ensure_index({'key_query':'text'})
                self.tweet_collection.create_index([("key_track", 'text')])
                dic = {"END": -1};
                self.output_queu.put(dic);
                break
            self.__processingTweet(tweet)
            self.tweet_queue.task_done()
        
        process_dataWriter.join();
            
    
    def __processingTweet(self, tweet):
        clean_tweet = tweetUtils.processTweet(tweet)            
        sentiment_score = self.nb_classiffier.predict([clean_tweet])
        tweet_split = clean_tweet.split()
        query_split = self.track_query[0].split(",")
       
        # We consider the fact that in a tweet can appear several query terms
        for key in query_split:
            if key.lower() in tweet_split:  
            #if key.lower() in tweet_split:      
                data ={}
                data['text'] = clean_tweet
                data['key_track'] = key
                data['SA_score'] = sentiment_score;
                self.tweet_collection.insert(data)
                dic = {}
                dic[key] = sentiment_score[0];
                self.output_queu.put(dic);
        
    def __runDataWriter(self):
        writer = PartialDataWriter(self.output_queu, self.file_partialResult,2)
        writer.run()