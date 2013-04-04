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


def updatefollowers(api=None,file_path="/DataFiles/followers.txt"):##a file for followers list, indicate the start date of following, and wether or not Direct message (invitation) has been sent
       
    followers=return_followers(file_path);
    #read for new followers
    cursor = -1
    while cursor!=0:
        ret = api.GetFollowers(cursor=cursor)
        users=ret["users"]      
        for user in users:
            uid=user['id']
            if not uid in followers:
                followers[uid]=[date.today(),0]
        cursor=ret["next_cursor"]
    #update the local followers list
    write_var_in_file(followers,file_path)
    return followers


def return_followers(file_path="/DataFiles/followers.txt"):
    followers={}
    #check if the followers file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            followers=cpik.loads(handle.read())
    return followers


def write_var_in_file(followers={},file_path=None):
    with open(file_path,'wb') as handle:
        cpik.dump(followers,handle)


if __name__=='__main__':
    print '********Update Followers*********'+str(datetime.date.today())+'*****************'     
    my_screen="auth_user"
    api=Auth.get_authentication(my_screen)
    updatefollowers(api=api)
    print '***************** END *****************'

    
    
