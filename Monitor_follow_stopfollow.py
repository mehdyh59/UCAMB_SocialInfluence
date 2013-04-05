import Auth
import datetime
import cPickle
import os
import twitter
import pp
import time
import tempfile

def fetch_data(screen_name=None,ids=[]):
    api=Auth.get_authentication(screen_name=screen_name)
    list_pairs={}
    out_path='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/Users/pairs'#
    if os.path.exists(out_path):
        with open(out_path,'rb') as handle:
            list_pairs=cPickle.loads(handle.read())
    if len(list_pairs)>0:
        extract = lambda data, sampled_data: dict(zip(data, map(sampled_data.get, data)))
        list_pairs=extract(ids,list_pairs)
    current_time=datetime.datetime.now()   
    for ID in ids:
        try:
            usr=api.GetUser(ID)
            nFollows=usr.GetFollowersCount()
            nFriends=usr.GetFriendsCount()
            nStatus=usr.GetStatusesCount()
            if nFollows==None or nFriends==None or nStatus==None:
                continue
            if list_pairs.has_key(ID):
                if list_pairs[ID]!=None:
                    list_pairs[ID].append((nFollows,nFriends,nStatus,current_time))
            else:
                list_pairs[ID]=[(nFollows,nFriends,nStatus,current_time)]

        except twitter.TwitterError, ex:
            print ex.message
            if "Clients may not make more than 350 requests per hour" in ex.message:
                print screen_name
                break
            else:
                continue
            
    print 'done!!!'
    return list_pairs


def parll_crawl():
    ids=[]

    ppservers=()
    job_server=pp.Server(ppservers=ppservers)
    #print "Starting pp with", job_server.get_ncpus(), "workers"
    lst=[]
    pairs={}
    if os.path.exists(out_path):
        with open(out_path,'rb') as handle:
            data=cPickle.loads(handle.read())
    else:
        with open(in_path,'rb') as handle:
            data=cPickle.loads(handle.read())
    ids=data.keys()
    L=len(ids)
    chunk_l=(int)(L/len(accounts))
    for i in range(0,len(accounts)):
        if i<len(accounts)-1:
            lst.append(ids[i*chunk_l:(i+1)*chunk_l])
        else:
            lst.append(ids[i*chunk_l:L])
    jobs=[job_server.submit(func=fetch_data,args=(accounts[i],lst[i],),modules=('Auth','datetime','cPickle','os','twitter',)) for i in range(0,len(accounts))]
    for job in jobs:
        result=job()
        if isinstance(result,dict):
            pairs=dict(pairs, **result)
    
    with open(out_path,'wb') as handle:
        cPickle.dump(pairs,handle)
    
tempfile.tempdir='/local/scratch/mh717'
accounts=['baradarekhoob','madarekkhoob','khaharekhoob','DokhtarKhoob']#'pedare_khoob', 'Pesare_Khoub',
out_path='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/Users/pairs'#
in_path='/home/mh717/Research_Cambridge/SocialInfluence/Codes/DataFiles/Users/sampled_usersDB2'#sampled_usersDB1 test
print "##Begin#########"+str(datetime.datetime.now())+"##########"
parll_crawl()
print "###End########"+str(datetime.datetime.now())+"##########"
