# (C) 2014 iMath Research S.L. - All rights reserved.
'''
    This class offers several services required to preprocess a tweet

Authors:

@author iMath
'''
from TwitterTracking.core.constants import CONS
import re
from string import punctuation

C = CONS()

class TweetUtils(object):
    
    def __init__(self):
        self.stopwords = self.__getStopWordList(C.STOPWORDS_FILE)
    
      
    def processTweet(self, tweet):
            
        #Convert to lower case
        tweet = tweet.lower()
        
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','USER',tweet)
        #Remove retweets
        tweet = re.sub(r'\brt\b', ' ', tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
            
        for p in list(punctuation):        
            tweet = tweet.replace(p, '')
    
        tweet = tweet.split()
        processed_tweet = ''
        for word in tweet:
            #check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word)
            if(word in self.stopwords or val is None):
                #ignore if it is a stop word
                continue
            else:
                w = self.__replaceTwoOrMore(word)
                processed_tweet = processed_tweet + w + ' '
    
        #Remove additional white spaces
        processed_tweet = re.sub('[\s]+', ' ', processed_tweet)
    
        return processed_tweet


    def __getStopWordList(self, stopWordListFileName):
        #read the stopwords file and build a list
        stopWords = []
        stopWords.append('USER')
        stopWords.append('URL')
 
        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        
        fp.close()
        return stopWords



    def __replaceTwoOrMore(self, word):
        #look for 2 or more repetitions of character and replace with the character itself
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", word)

 

