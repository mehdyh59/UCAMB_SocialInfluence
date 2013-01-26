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


def updatefriends(api=None,file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/friends.txt"):##a file for friends list, indicate the start date of following the friend, and wether or not the friend is removed from the friend list: 0 means not removed yet and 1 means removed
    friends=return_friends(file_path)
    #read for new friends
    cursor = -1
    while cursor!=0:
        ret = api.GetFriends(cursor=cursor)
        users=ret["users"]      
        for user in users:
            uid=user['id']
            if not uid in friends:
                friends[uid]=[date.today(),0]
        cursor=ret["next_cursor"]

    #update the local followers list 
    write_var_in_file(friends,file_path)
    return friends

def return_friends(file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/friends.txt"):
    friends={}
    #check if the friends file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            friends=cpik.loads(handle.read())
    return friends

def write_var_in_file(followers={},file_path=None):
    with open(file_path,'wb') as handle:
        cpik.dump(followers,handle)


if __name__=='__main__':
    print '********Update Friends*********'+str(datetime.date.today())+'*****************'        
    my_screen="data1_surgeon"
    api=Auth.get_authentication(my_screen)
    updatefriends(api=api)
    print '***************** END *****************'

    
    
