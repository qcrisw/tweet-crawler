# 
# tasks.py
# 
# this file contains a set of task function
# definitions which can be used with TaskQueue
# objects to asynchronously execute background
# jobs/tasks
# 
import os

from databases import MongoDB

def mongo_add_tweets(batch, url=os.environ['MONGO_URL']):
    '''write a list of tweets to MongoDB'''
    driver = MongoDB(url)
    driver.add_tweets(batch)

def print_hello():
    print('hello!')
