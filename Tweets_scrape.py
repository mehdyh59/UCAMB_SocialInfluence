import Auth
import cPickle as cpik
import os
import tempfile


def scrape(partic_file='DataFiles/paricipants.txt'):
    participants=return_participants(file_path=partic_file)
    my_screenname='data1_surgeon'
    out_path='DataFiles/Tweets/'
    api=Auth.get_authentication(screen_name=my_screenname)
    max_twt_count=10
    count=5
    bb=0

    
    for part in participants:
        counter=0
        tweets=[]
        max_twt_id=None
        
        try:
            user_id=int(part)
            user=api.GetUser(user_id)
            tweets_count=user.statuses_count
        except twitter.TwitterError, ex:
            print ex.message
            continue
        threshold=min([max_twt_count,tweets_count])
        while counter<threshold:
            try:
                temp=api.GetUserTimeline(user_id=user_id,max_id=max_twt_id,include_entities=True,count=count,include_rts=True)
                counter+=len(temp)
                tweets+=temp
                max_twt_id=return_maxID(tweets=temp)
            except twitter.TwitterError , ex:
                print ex.message
                break
            if max_twt_id==None:
                break
        file_name=out_path+str(part)
        with open(file_name,'wb') as handle:
            cpik.dump(tweets,handle)
        print 'done with '+str(part)
        bb+=1
        if bb>15:
            break

def return_maxID(tweets=None):
    ids=[]
    for tweet in tweets:
        ids+=[tweet.id]
    min_id=None
    if len(ids)>0:
        min_id=min(ids)
        min_id-=1
    return min_id
    

def return_participants(file_path="DataFiles/paricipants.txt"):
    participants=set()
    #check if the file exists
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            participants=cpik.loads(handle.read())
    return participants

if __name__=='__main__':
    tempfile.tempdir='/local/scratch/mh717'
    scrape()
