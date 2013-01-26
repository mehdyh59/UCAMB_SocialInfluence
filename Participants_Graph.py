import Auth
import datetime
import cPickle as cpik
import os
import numpy as np
import random
import twitter

def check_in(in_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/sub_paricipants.txt",out_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/"):
    screen_names=['mehdy_h59','data1_surgeon','mana_macaron','CoxA59']
    
    checked_participants_file='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/checked.txt'
    notauthorized_participants_file='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/notAuthorized.txt'

    while len(screen_names)>0:
        screen_name=screen_names.pop()

        print screen_name

        participants=return_participants(file_path=in_path)
        #print len(participants)
        if os.path.exists(checked_participants_file):
            with open(checked_participants_file,'rb') as  handle:
                checked_partice=cpik.loads(handle.read())
                participants=participants-checked_partice

        if os.path.exists(notauthorized_participants_file):
            with open(notauthorized_participants_file,'rb') as  handle:
                checked_partice=cpik.loads(handle.read())
                participants=participants-checked_partice

        if len(participants)==0:
            if os.path.exists (checked_participants_file):
                os.remove(checked_participants_file)
            if os.path.exists (notauthorized_participants_file):
                os.remove(notauthorized_participants_file)                
            print 'successfully finittto! beginning next round!'
        api=Auth.get_authentication(screen_name=screen_name)
        status=recored_participants_graphs(api=api,participants=participants)
##        if type(status)==str and status=='failed':
##            continue
##        else:
##            part1=set([])
##            part2=set([])
##            if os.path.exists(checked_participants_file):
##                with open(checked_participants_file,'rb') as handle:
##                    part1=cpik.loads(handle.read())
##            if os.path.exists(notauthorized_participants_file):
##                with open(notauthorized_participants_file,'rb') as handle:
##                    part2=cpik.loads(handle.read())
##            part=set.union(part1,part2)
##            if participants==part:
##                os.remove(checked_participants_file)
##                print 'successfully finittto!'
##                break
##            else:
##                continue

def recored_participants_graphs(api=None,in_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/paricipants.txt",out_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/",participants=set(),checked_participants_file='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/checked.txt',NotAuthorized_participants_file='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/notAuthorized.txt'):
    today=datetime.datetime.today()
    checked_partice=set()
    notAuthorized_partice=set()
    for participant in participants:
        print 'go!!! '+ str(participant)
        try:
            usr=api.GetUser(participant)
            #recored_users_single(user=usr,ID=participant)
        except twitter.TwitterError, ex:
            print ' problem with '+str(participant)+' '+ex.message
            _update_checked_participants(set([participant]),NotAuthorized_participants_file)
            continue
        status=manage_graph(api=api,participant=participant,file_path=out_path,today=today)
        if type(status)==str and status=='failed':
            #_update_checked_participants(checked_partice,checked_participants_file)
##            if len(notAuthorized_partice)>0:
##                _update_checked_participants(notAuthorized_partice,NotAuthorized_participants_file)
            return status
        if type(status)==str and status=='Not authorized':
            _update_checked_participants(set([participant]),NotAuthorized_participants_file)
            #notAuthorized_partice.add(participant)
            #print str(participant)+"Not authorized!"
##        if type(status)==str and status=="ret[users] error":
##            continue
##        if type(status)==dict:
##            checked_partice.add(participant)
            #print str(participant)+" checked in!"        
    return 'succeed'

def manage_graph(api=None,participant=None,file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/",today=None):
    if participant==None:
        return 'succeed'
    friends_file=file_path+'friends_'+str(participant)
    followers_file=file_path+'followers_'+str(participant)
    friends=_read_data(friends_file)
    followers=_read_data(followers_file)
    status=manage_friends(api=api,participant=participant,friends=friends,today=today)
    if type(status)==str:
        return status
    if type(status)==dict:
        friends=status

    status=manage_followers(api=api,participant=participant,followers=followers,today=today)
    if type(status)==str:
        return status
    if type(status)==dict:
        followers=status

    _update_checked_participants(set([participant]))
    _write_data(file_path=friends_file,data=friends)
    _write_data(file_path=followers_file,data=followers)
    print str(participant)+' is done!'
    return status

def manage_friends(api=None,participant=None,friends={},today=None):
    cursor=-1
    fresh_fri_ids=set()
    while cursor!=0:
        dict_users={}
        try:
            ret=api.GetFriends(user=participant,cursor=cursor)
        except Exception, ex:
            print ex.message
            if 'Not authorized' in ex.message:
                return 'Not authorized'
            else:
                return 'failed'
        try:
            users=ret['users']
        except Exception, ex:
            print str(participant)+ ex.message
            return 'ret[users] error'

        for user in users:
            uid=user['id']
            fresh_fri_ids.add(uid)
            dict_users[str(uid)]=user
            if not uid in friends:
                friends[uid]=[today]
            else:
                if np.mod(len(friends[uid]),2)==0:
                    friends[uid].append(today)
        cursor=ret["next_cursor"]
        #recored_users_batch(users=dict_users)
    if friends!=None:
        for fkey in friends:
            if not fkey in fresh_fri_ids:
                friends[fkey].append(today)
    return friends

def manage_followers(api=None,participant=None,followers={},today=None):
    cursor=-1
    fresh_fol_ids=set()
    while cursor!=0:
        dict_users={}
        try:
            ret=api.GetFollowers(user=participant,cursor=cursor)
        except Exception, ex:
            print ex.message
            if 'Not authorized' in ex.message:
                return 'Not authorized'
            else:
                return 'failed'
        try:
            users=ret['users']
        except Exception, ex:
            print str(participant)+ ex.message
            return 'ret[users] error'
        for user in users:
            uid=user['id']
            fresh_fol_ids.add(uid)
            dict_users[str(uid)]=user
            if not uid in followers:
                followers[uid]=[today]
            else:
                if np.mod(len(followers[uid]),2)==0:
                    followers[uid].append(today)
        #recored_users_batch(users=dict_users)
        cursor=ret["next_cursor"]
    if followers!=None:
        for fkey in followers:
            if not fkey in fresh_fol_ids:
                followers[fkey].append(today)
    return followers


def _update_checked_participants(new_checked=set(),checked_participants_file='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/participants/checked.txt'):
    old_checked=set()
    if os.path.exists(checked_participants_file):
        with open(checked_participants_file,'rb') as handle:
            old_checked=cpik.loads(handle.read())
    checked=set.union(old_checked,new_checked)

    with open(checked_participants_file,'wb') as handle:
        cpik.dump(checked,handle)

def _read_data(file_path=None):
    data={}
    if os.path.exists(file_path):
        with open(file_path,'rb') as  handle:
            data=cpik.loads(handle.read())
    return data

def _write_data(file_path=None,data=None):
    with open(file_path,'wb') as handle:
        cpik.dump(data,handle)

def return_participants(file_path="/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/paricipants.txt"):
    participants=set()
    #check if the file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            participants=cpik.loads(handle.read())
    return participants

def recored_users_single(user={},ID=None,users_path='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/Users/usersDB'):
    data={}
    if os.path.exists (users_path):
        with open(users_path,'rb') as handle:
            data=cpik.loads(handle.read())       
    data[ID]=user
    with open(users_path,'wb') as handle:
        cpik.dump(data,handle)

def recored_users_batch(users={},users_path='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/Users/usersDB'):
    data={}
    if os.path.exists (users_path):
        with open(users_path,'rb') as handle:
            data=cpik.loads(handle.read())
    data.update(users)
    with open(users_path,'wb') as handle:
        cpik.dump(data,handle)


if __name__ == '__main__':
    print '*******Update_Participants_Graph**********'+str(datetime.datetime.today())+'*****************'
    check_in()
    #print 'test!'
    print '***************** END *****************'
