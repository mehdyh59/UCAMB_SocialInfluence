import Auth
import urllib2
from sets import Set
from datetime import date
import cPickle as cpik
import os
import random
import csv
import datetime
import twitter
import sys
import tempfile


def follow_people(screen_name,max_friend=10,api=None,file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/friends.txt"):
    ###follow people who are following a particular Twitter user
    today=datetime.date.today()
    friends=return_friends()
    followers=return_followers()
    participants=return_participants()
    new_friends={}
    cursor = -1
    counter=0
    while cursor!=0 and counter<max_friend:
        ret = api.GetFollowers(user=screen_name,cursor=cursor)
        users=ret["users"]      
        for user in users:
            uid=user['id']
            if (not uid in friends) and (not uid in followers) and (not uid in participants) and IsQualified(user=user):
                try:
                    api.CreateFriendship(uid)
                    counter+=1
                    new_friends[uid]=[today,0]
                    #print str(uid)+' was followed!'
                except twitter.TwitterError, ex:
                    print ex.message
                    continue
            if counter>max_friend:
                break
        cursor=ret["next_cursor"]
    write_new_friends(new_friends)
    print str(counter)+' people were followed!'
    return counter
    

def return_followers(file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/followers.txt"):
    followers={}
    #check if the followers file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            followers=cpik.loads(handle.read())
    return followers


def return_friends(file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/"):
    path1=file_path+'friends.txt'
    path2=file_path+'friends_14Feb.txt'
    friends1={}
    friends2={}
    #check if the friends file exists
    if os.path.exists(path1):
        with open(path1,'rb') as handle:
            friends1=cpik.loads(handle.read())
    if os.path.exists(path2):
        with open(path2,'rb') as handle:
            friends2=cpik.loads(handle.read())
    friends=dict(friends1.items()+friends2.items())
    return friends

def return_participants(file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/paricipants.txt"):
    participants=set()
    #check if the file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            participants=cpik.loads(handle.read())
    return participants


def write_var_in_file(followers={},file_path=None):
    with open(file_path,'wb') as handle:
        cpik.dump(followers,handle)

def write_new_friends(new_friends={},file_path='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/friends.txt'):
    with open(file_path,'rb')as handle:
        friends=cpik.loads(handle.read())
    friends=dict(friends.items()+new_friends.items())
    with open(file_path,'wb') as handle:
        cpik.dump(friends,handle)


def IsQualified(user=None,down_followers=30,up_followers=100000,ratio=4,deadline='2012-08-01'):#checks a twitter user and tests if the user is qualified to be followed
    deadline=datetime.datetime.strptime(deadline,"%Y-%m-%d")
    num_followers=user['followers_count']
    num_friends=user['friends_count']
    if num_friends>0:
        r=float(num_followers)/float(num_friends)
    else :
        return False
    uid=user['id']
    tweet_date=None
    if user.has_key('status'):
        status=user['status']
        if status!=None and status.has_key('created_at'):
            tweet_date=status['created_at']
    if tweet_date!=None:
        tweet_date=tweet_date.replace('+0000','')
        tweet_date=datetime.datetime.strptime(tweet_date,'%a %b %d %H:%M:%S %Y')              
    else:
        tweet_date=deadline
    tweet_count=0
    if user.has_key('statuses_count'):
        tweet_count=user['statuses_count']
    if (num_followers<down_followers or num_followers>up_followers or r >= ratio or tweet_date<deadline or tweet_count<=0):
        return False
    return True

if __name__ == '__main__':
    tempfile.tempdir='/local/scratch/mh717'
    if len(sys.argv)>1:
        my_screen=sys.argv[1]
    else:
        my_screen="data1_surgeon"
    print '******Following***********'+str(datetime.datetime.today())+'*****************'+my_screen
    toss=random.random()
    if toss<0.9:
        api=Auth.get_authentication(my_screen)
        #repository=['UNICEF','VolunteerGlobal','VolunteerCal','VolunteerTO','VolunteerMatch','AmericanCancer','AllHands','VolunteeringEng','MindCharity','AskMen','UN_Women','David_Cameron','googleresearch','BradPittsPage','BillGates','BarackObama','facebook','CommunityCare','hootsuite','mashable','TheNextWeb','Donnaantoniadis','NielsenWire','adidasoriginals','iTunesMusic','UniversalMusica','HuffPostWomen','womenoffaith']
        repository=['BBCBreaking','cnnbrk','rihanna','Olympics','socialmedia2day','VolunteerCanada','ChampionsLeague','QueenLizII','kate_middleton','DukeCambridgeUK']
        max_friend=int(round(15+(26-15)*random.random()))
        n_followed=0
        while n_followed<max_friend and len(repository)>0:
            rnd_index=int(round(random.random()*(len(repository)-1)))
            n_followed=follow_people(repository[rnd_index],max_friend,api=api)
            if n_followed<max_friend:
                repository.remove(repository[rnd_index])
    else:
        print 'skipped!'

    print '***************** END *******' +my_screen +'*****************'
