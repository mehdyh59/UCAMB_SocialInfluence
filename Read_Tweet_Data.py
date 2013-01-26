import simplejson, urllib

def read_tweet_users_data():
    url='http://api.twitter.com/1/statuses/followers/kdnuggets.json';
    users=simplejson.load(urllib.urlopen(url));
    #print users;
    print len(users);
    for user in users:
        print user['name']+'\n';


    
read_tweet_users_data();
