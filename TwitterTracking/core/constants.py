'''
Created on 11/11/2013

@author: iMath
'''


def constant(f):
    '''
    Decorator to indicate that a property of a class is a constant, so, cannot be set, only get
    '''
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)


class CONS(object):
    '''
    It define the global constants for the Twitter Tracker
    These constants must be set to the values associated to an iMath account in Twitter 
    
    '''
    @constant
    def CONSUMER_KEY():
        return 'NIPqiUBMkGgEPsZTUGvWzIAGv'
    
    @constant
    def CONSUMER_SECRET():
        return '6Qb6eX8c6lOg7Vuh1ageW92ucddylC7unytJ3crJTBYgdVARcW'
    
    @constant
    def ACCESS_TOKEN():
        return '519460742-P9llilYNcuy1VUtuASOnHOFhJStJyuiD75M18mEZ'
    
    @constant
    def ACCESS_TOKEN_SECRET():
        return '8jGzEMsrkuT5nvuxnmp8Zcpt9WM6Xdxm3F3OCpUafLMw8'
    
    @constant
    def TWITTER_DB():
        return "test_db"
    
    @constant
    def TOKEN_LAST_TWEET():
        return 'LAST_ELEMENT'
    
    @constant
    def STOPWORDS_FILE():
        return '/home/andrea/workspace/twitter_Tracking/TwitterTracking/core/util/stopwords.txt'
        
        
        