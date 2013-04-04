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


def send_invitation(api=None,sample_size=30,file_path="",days=4):
    orig_text="a 2 min Twitter survey run by researchers at ComputerLab Cambridge University. If interested, follow the link! "
    orig_url="www.cl.cam.ac.uk/~mh717/survey_Twitter/intro.html?esm="
    #read local followers
    followers=return_followers(file_path)
    today=date.today();
    deldate=today-datetime.timedelta(days=days)

    #sample a subset of followers
    sampled_followers=sample_to_invite(sample_size,followers,deldate)
    for usrID in sampled_followers:
        ID=inverse_id(usrID)
        url=orig_url+ID;
        url=urllib2.quote(url.encode("utf8"))
        text=orig_text+url;
        try:
            api.PostDirectMessage(usrID,text)
            #print str(usrID)+" invited!"
        except twitter.TwitterError, ex:
            print 'User ID: '+str(usrID)+' '+ex.message
            continue
    update_invitation(sampled_followers,followers,file_path=file_path)
    print str(sample_size)+' people were invited!'

def return_followers(file_path=""):
    followers={}
    #check if the followers file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            followers=cpik.loads(handle.read())
    return followers

def sample_to_invite(n=30,followers={},deldate=None): 
    followers=get_non_invted_followers(followers,deldate)
    N=len(followers)
    if n>N:
        return followers
    else:
        sample_followers={}
        keys=followers.keys()
        for i in xrange(1,n):
            keyid=random.randint(0,len(keys)-1)
            key=keys[keyid]
            sample_followers[key]=followers[key]
            keys.remove(key)
        return sample_followers

    
def get_non_invted_followers(followers={},deldate=None):
    non_inv_followers={}
    participants=return_participants()
    #print deldate
    for key,item in followers.iteritems():
        if item[0]<=deldate and item[1]==0 and not str(key) in participants: 
            non_inv_followers[key]=item
    #print non_inv_followers
    return non_inv_followers

def return_participants(file_path=""):
    participants=set()
    #check if the file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            participants=cpik.loads(handle.read())
    return participants

def update_invitation(sampled_followers={},followers={},file_path=""):
    for key,items in sampled_followers.iteritems():
        items[1]=1
        followers[key]=items
    write_var_in_file(followers,file_path=file_path)

def write_var_in_file(followers={},file_path=None):
    with open(file_path,'wb') as handle:
        cpik.dump(followers,handle)

def inverse_id(uid):
    uid=list(str(uid))
    uid.reverse()
    uid=''.join(uid)
    return uid

if __name__=='__main__':
    print '********Invitation*********'+str(datetime.datetime.today())+'*****************'  
    my_screen="data1_surgeon"
    api=Auth.get_authentication(my_screen)
    send_invitation(api=api,sample_size=250,file_path="/DataFiles/followers.txt",days=3)
    print '***************** END *****************'

