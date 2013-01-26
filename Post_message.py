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

#Researcher, ComputerLab, Cambridge University. Running a 2 minutes survey as a part of a project on Social Network. If interested, follow the link below.
#data1_surgeon
##con_key='95xlaFoKBsebx6dVUh9WSw'
##con_sec='ERNTKp0m1SvaXi3Y6NIF97JKIp4pn2DiTOvR3vVGR1U'
##acc_tok='897433675-1EdKl4xnaxImIG2uf95CXoH25xGfIEfO5H7GxRz4'
##acc_sec='lqXp0hPX5FkKQPych8mAbPNE1tm6Gfj2LuCdGyaViM'
##my_screen='data1_surgeon'

#mehdy_h59
##con_key='49Jf6XcYS6nFfDAnD8OxA'
##con_sec='Ny7hLvcGNCfafcJykkPpFED350BQ0JjrweOJcVsJs'
##acc_tok='34409944-kRuM7yKAqsAR1x7PROK6PPH0VWdIKu3ds4cIV8Oz0'
##acc_sec='jX2ZwxgkV3pg3M8z2FAfoQ50zIgvLnrw2frLVbr9E'


def follow_people(screen_name,max_friend=20,api=None,file_path="DataFiles/friends.txt"):#follow people who are following a particular Twitter user
    today=datetime.date.today()
    #update_friends(api,file_path)
    friends=return_friends()
    followers=return_followers()
    participants=return_participants()
    
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
                    friends[uid]=[today,0]
                    print counter
                except twitter.TwitterError, ex:
                    print ex.message
                    continue
        cursor=ret["next_cursor"]
    #update the local followers list
    write_var_in_file(friends,file_path)
    

def search_users(api=None,query=None,max_results=100):
    users=[]
    page=1
    while page!=0 and len(users)<max_results:
        result=api.SearchUsers(query=query,page=page)
        if len(result)>0:
            users+=result
            page+=1
        else:
            page=0
    return users
    

def return_followers(file_path="DataFiles/followers.txt"):
    followers={}
    #check if the followers file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            followers=cpik.loads(handle.read())
    return followers


def return_friends(file_path="DataFiles/friends.txt"):
    friends={}
    #check if the friends file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            friends=cpik.loads(handle.read())
    return friends

 
def update_friends(api=None,file_path="DataFiles/friends.txt"):##a file for friends list, indicate the start date of following the friend, and wether or not the friend is removed from the friend list: 0 means not removed yet and 1 means removed

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

def update_followers(api=None,file_path="DataFiles/followers.txt"):##a file for followers list, indicate the start date of following, and wether or not Direct message (invitation) has been sent
       
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

def update_participants(in_path="Results/integerated_2q_rnd2.csv",out_path="DataFiles/paricipants.txt"):
    participants=return_participants(out_path)
    #participants=set()
    try:
        inp_reader = csv.reader(open(in_path, 'rb'), delimiter=',')
    except IOError, ex:
        print "The {%s} not found: I/O Error ({%d}):{%s}" % (in_path,ex.errno, ex.strerror)
    counter=0
    for row in inp_reader:
        counter+=1
        if counter>2 and len(row)>1 and len(str(row[2]))>0:
            #print row[2]
            uid=inverse_id(row[2])
            participants.add(uid)
    write_var_in_file(participants,out_path)
        
def return_participants(file_path="DataFiles/paricipants.txt"):
    participants=set()
    #check if the friends file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            participants=cpik.loads(handle.read())
    return participants
    

def send_invitation(api=None,sample_size=30,file_path="DataFiles/followers.txt",days=4):

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
            print str(usrID)+" invited!"
        except twitter.TwitterError, ex:
            print 'User ID: '+str(usrID)+' '+ex.message
            continue
    update_invitation(sampled_followers,followers)

def _send_invit_test(usrID,api=None,file_path="DataFiles/followers.txt"):

    orig_text="a 2 min Twitter survey run by researchers at ComputerLab Cambridge University. Your contribution will be appreciated! "
    orig_url="www.cl.cam.ac.uk/~mh717/survey_Twitter/intro.html?esm="
    today=date.today();
    ID=list(str(usrID))
    ID.reverse();
    ID="".join(ID);
    url=orig_url+ID;
    url=urllib2.quote(url.encode("utf8"))
    text=orig_text+url;
    api.PostDirectMessage(usrID,text)
    print 'invitation sent!'

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

def print_invited_followers(api=None,followers={}):
    counter=0;
    for follower,item in followers.iteritems():
        if item[1]==1:
            try:
               user=api.GetUser(int(follower))
            except twitter.TwitterError, ex:
                print ex.message
                counter+=1
                continue
            print follower,user.GetScreenName()
            counter+=1
    print "num invited: "+str(counter)

def update_invitation(sampled_followers={},followers={}):
    for key,items in sampled_followers.iteritems():
        items[1]=1
        followers[key]=items
    write_var_in_file(followers,"DataFiles/followers.txt")
    

def write_var_in_file(followers={},file_path="DataFiles/followers.txt"):
    with open(file_path,'wb') as handle:
        cpik.dump(followers,handle)

def fresh_the_followersList(api=None):#get the list of followers ID from Twitter
    followers=[]
    #read the fresh list of followers
    cursor = -1
    while cursor!=0:
        ret = api.GetFollowers(cursor=cursor)
        users=ret["users"]      
        for user in users:
            uid=user['id']
            if not uid in followers:
                followers+=[uid]
        cursor=ret["next_cursor"]
    #update the local followers list
    return followers

def fresh_the_friendsList(api=None):#get the list of friends ID from Twitter
    friends=[]
    #read the fresh list of followers
    cursor = -1
    while cursor!=0:
        ret = api.GetFriends(cursor=cursor)
        users=ret["users"]      
        for user in users:
            uid=user['id']
            if not uid in friends:
                friends+=[uid]
        cursor=ret["next_cursor"]
    #update the local followers list
    return friends

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


def stop_following_friends(api=None, deadline=20,life_deadline=9000000,file_path='DataFiles/friends.txt'):
#stop following people who are not following you back and given enough number of days (specified by deadline) 
    delta=datetime.timedelta(days=deadline)

    delta_date=datetime.datetime.today()-delta
    delta_date=delta_date.date()
    friends=return_friends()

    life_delta=datetime.timedelta(days=life_deadline)
    life_delta_date=datetime.datetime.today()-life_delta
    life_delta_date=life_delta_date.date()
        
    #followers=update_followers(api,file_path)
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
                print str(fid)+ ' removed!'
                c+=1
            except twitter.TwitterError, ex:
                print ex.message
    write_var_in_file(friends,file_path)
    print str(c)+' were removed!'


def MailedResponses_Set_TweetID(api=None,file_path='Results/survey_results_mailed_5.csv'):
    data=[]
    try:
        inp_reader = csv.reader(open(file_path, 'rb'), delimiter=',')
    except IOError, ex:
        print "The {%s} not fotwitter api get direct message page countund: I/O Error ({%d}):{%s}" % (file_path,ex.errno, ex.strerror)
    counter=0
    for row in inp_reader:
        print row
        counter+=1
        if counter>2 and len(row[32])>0:
            screen_name=row[32]
            screen_name=screen_name.strip()
            if len(screen_name)>0:
                if screen_name.startswith('@'):
                    screen_name=screen_namwrite_var_in_filee[1:len(screen_name)]
                    screen_name=screen_name.strip()
            try:
                user=api.GetUser(screen_name)
                uid=user.GetId()
                uid=inverse_id(uid)
                row[2]=uid
            except twitter.TwitterError, ex:
                print ex.message
                continue
        data.append(row)
    
    with open(file_path,'wb') as fln:
            csv.writer(fln).writerows(data)

def return_invited_people(api=None):
    page=1
    guests=set()
    msgid=[]
    while True:
        msgc=0
        try:
            msgs=api.Get_Sent_Messages(page=page,count=1)
            if len(msgs)==0 or msgs==None:
                break
            for msg in msgs:
                guests.add(msg['recipient_id'])
                if not msg['id'] in msgid:
                    msgc+=1
                    msgid+=[msg['id']]
            page+=1
            if msgc==0:
                print 'looping the same msgs list'
                break
        except twitter.TwitterError, ex:
            print ex.message
    return guests
            
def inverse_id(uid):
    uid=list(str(uid))
    uid.reverse()
    uid=''.join(uid)
    return uid

##api=twitter.Api(consumer_key=con_key,consumer_secret=con_sec,access_token_key=acc_tok,access_token_secret=acc_sec)
my_screen='mehdy_h59'#"data1_surgeon"
api=Auth.get_authentication(my_screen)
######path="DataFiles/friends.txt"
########screen_name=['David_Cameron','googleresearch','BradPittsPage','BillGates']
########max_friend=200
#usr=api.GetUser(123201468)#(18137777)
#usrID=usr.GetScreenName()
####usrID=inverse_id(usrID)
#print usrID
##users=search_users(api,query='volunteer Uk',max_results=20)
##n_followers=[]
##for user in users:
##    print user['screen_name'], user['followers_count']
##    n_followers+=[user['followers_count']]
##print 'min: '+ str(min(n_followers))

#print usrID
#_send_invit_test(usrID,api=api,file_path=path)

#print len(return_participants())
#print(len(f))
##stop_following_friends(api,deadline=1,life_deadline=20)

#update_friends(api)
##for i in range(len(screen_name)):
##    follow_people(screen_name[i],max_friend,api=api)

#MailedResponses_Set_TweetID(api=api,file_path='Results/survey_results_emailed_5ans.csv')
#update_participants(in_path='Results/integerated_2q_rnd2.csv')

#_send_invit_test(usrID=usrID,api=api)
#send_invitation(api,sample_size=250,days=2)

#print len([fitem for fitem in return_followers().values() if fitem[1]==0])

#f=update_friends(api=api)
#print len(f)
##pp=return_participants()
##pp.remove('6708263')
##print len(pp)
##with open('DataFiles/paricipants.txt','wb') as handle:
##    cpik.dump(pp,handle)


with open('DataFiles/participants/checked.txt','rb') as handle:#notAuthorized   checked
    print len(cpik.loads(handle.read()))
##
#print len(return_participants('DataFiles/sub_participants.txt'))
#print len(parts)
##for part in parts:
##    print type(part)
##    break

##add_data=['920636778','615126132','136361140','817500956','247049916','175065144','897433675','38231044','306760743','15013860','762546128','325552720'] 
##data=set.union(data,add_data)
##print len(data)


