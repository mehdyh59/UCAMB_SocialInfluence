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

def stop_following_friends(api=None, max_removed=10,deadline=20,life_deadline=9000000,file_path='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/friends.txt'):
#stop following people who are not following you back and given enough number of days (specified by deadline) 
    delta=datetime.timedelta(days=deadline)

    delta_date=datetime.datetime.today()-delta
    delta_date=delta_date.date()
    friends=return_friends()

    life_delta=datetime.timedelta(days=life_deadline)
    life_delta_date=datetime.datetime.today()-life_delta
    life_delta_date=life_delta_date.date()
        
    followers=return_followers()
    participants=return_participants()
    c=0
    for fid,fitem in friends.iteritems():
        fdate=fitem[0]
        if type(fdate)==datetime.datetime:
            fdate=fdate.date()
        removed=fitem[1]
        if ((not fid in followers.keys() and fdate<=delta_date) or (not str(fid) in participants and fdate<=life_delta_date)) and (not removed):
            try:
                api.DestroyFriendship(fid)
                friends[fid]=[fitem[0],1]
                #print str(fid)+ ' removed!'
                c+=1
                if c>=max_removed:
                    break;
            except twitter.TwitterError, ex:
                print ex.message
    write_var_in_file(friends,file_path)
    print str(c)+' were removed!'


def return_followers(file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/followers.txt"):
    followers={}
    #check if the followers file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            followers=cpik.loads(handle.read())
    return followers


def return_friends(file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/friends.txt"):
    friends={}
    #check if the friends file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            friends=cpik.loads(handle.read())
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

if __name__=='__main__':
    print '*******Stop_Following**********'+str(datetime.datetime.today())+'*****************'    
    toss=random.random()
    if toss<0.9:
        my_screen="data1_surgeon"
        api=Auth.get_authentication(my_screen)
        max_removed=int(round(15+(20-15)*random.random()))
        stop_following_friends(api=api,max_removed=max_removed,deadline=7,life_deadline=20)
    else:
        print 'skipped!'
    print '***************** END *****************'
    
    
