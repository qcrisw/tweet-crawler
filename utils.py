def get_full_text(status):
    '''Given a tweepy Status object, returns the full text of the tweet'''
    data = status._json
    
    # original tweet, > 140 characters
    if 'extended_tweet' in data:
        print(data['extended_tweet']['full_text'])
        
    # retweeted tweet...
    elif 'retweeted_status' in data:
        data = data['retweeted_status']

        # ... > 140 characters
        if 'extended_tweet' in data:
            print(data['extended_tweet']['full_text'])

        # ... <= 140 characters
        else:
            print(data['text'])

    # original tweet, <= 140 characters
    else:
        print(data['text'])
