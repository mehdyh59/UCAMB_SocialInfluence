import csv
import numpy as np
import scipy as sp
import cPickle as cpik
import matplotlib.pyplot as plt
import matplotlib
import Auth
import os
import numbers

class Survey():
    name=None
    start_time=None
    end_time=None
    duration=None
    IP=None
    gender=None
    age=None
    nationality=None
    answers=[]
    num_q=None

    def __init__(self,name='Twitter'):
        self.name=name

class Stats():
    n_friends=None
    n_followers=None
    n_tweets=None
    following_back_prop=None
    followed_back_prop=None
    common_followers_friends=None
    friends_followers={}
    friends_friends={}
    followers_friends={}
    followers_followers={}
    def __init__(self,n_fri=None,n_fol=None,n_twet=None):
        self.n_friends=n_fri
        self.n_followers=n_fol
        self.n_tweets=n_twet
       
    
class Participant():
    name=None
    screen_name=None
    ID=None
    survey=None
    stats=None

    def __init__(self,name=None,sname=None,ID=None):
        self.name=name
        self.screen_name=sname
        self.ID=ID

def get_stats(in_path="Results/Integerated.csv",out_path="DataFiles/stat_data.txt"):
    participants={}
    counter=0
    ques=[]
    sindex=11
    
    try:
        inp_reader=csv.reader(open(in_path,'rb'),delimiter=',')
    except IOError, ex:
        print "The {%s} not found: I/O Error ({%d}):{%s}" % (in_path,ex.errno, ex.strerror)
    for row in inp_reader:
        sindex=11
        usr=None
        if counter==0:
            ques=get_questions_list(row,sindex)
        if counter>=2:
            session_ID=row[0]
            if not session_ID in participants.keys():
                ID=row[2]
                if ID!='' or len(ID)!=0:
                    ID=inverse_id(row[2])
                    vID,usr=validate_id(ID)
                    if vID==-1:
                        vID,usr=validate_id(ID+'0')
                        if vID==-1:
                            continue
                    ID=vID
                ptc=Participant(ID=ID)
                ptc.survey=Survey()                
                if usr!=None:
                    ptc.stats=Stats(n_fri=usr.GetFriendsCount(),n_fol=usr.GetFollowersCount(),n_twet=usr.GetStatusesCount())
                    ptc.screen_name=usr.GetScreenName()
                    ptc.name=usr.GetName()
                ptc.survey.start_time=row[4]
                ptc.survey.end_time=row[5]
                ptc.survey.duration=row[6]
                ptc.survey.IP=row[7]
                ptc.survey.gender=row[8]
                ptc.survey.age=row[9]
                ptc.survey.nationality=row[10]
                answers=[]
                for i in range(0,len(ques)):
                    n_option=ques[i][1]
                    options=row[sindex:(sindex+n_option)]
                    answers.append(options)
                    sindex+=n_option
                #print answers
                ptc.survey.answers=answers
                participants[session_ID]=ptc
        counter+=1
    write_stat_data(participants,out_path)


def validate_id(ID=None):
    try:
        ID=int(ID)
    except Exception, ex:
        print ex.message
        return -1,None
    my_screen="data1_surgeon"
    api=Auth.get_authentication(my_screen)
    try:
        usr=api.GetUser(ID)
        s_name=usr.GetScreenName()
        
    except Exception, ex:
        print ex.message
        return -1,None
    if s_name==None:
        return -1,None
    else:
        return ID,usr
            
def inverse_id(uid):
    uid=list(uid)
    uid.reverse()
    uid=''.join(uid)
    return uid        
        
def get_questions_list(row,start_index=11):

    q=row[start_index]
    nq=0
    questions=[[q,1]]
    ctr=start_index+1
    while ctr < len(row):
        if row[ctr]==q:
            questions[nq][1]+=1
        else:
            q=row[ctr]
            nq+=1
            questions.append([q,1])
        ctr+=1
    return questions

def write_stat_data(participants,out_path="DataFiles/stat_data.txt"):        
    with open(out_path,'wb') as handle:
        cpik.dump(participants,handle)
    
def read_stat_data(in_path="DataFiles/stat_data.txt"):
    participants={}
    with open(in_path,'rb') as handle:
        participants=cpik.loads(handle.read())
    return participants

def draw_pie_chart(data=None,colors=None,labels=None,autopct='%1.1f%%',figno=1):
    plt.figure(figno)
    plt.pie(data,labels=labels,autopct=autopct,colors=colors)
    

def draw_bar_chart(index=[],values=[],width=0.35,color='k',title='',ylabel='Frequency',xlabel='Ages',xticks=[],xticklabels=(),figno=1,yerr=None,legend=[]):
    figo=plt.figure(figno)
    plt.bar(index,values,width=width,color=color,yerr=yerr)
    fig=figo.add_subplot(111)
    fig.set_ylabel(ylabel)
    fig.set_xlabel(xlabel)
    fig.set_title(title)
    #fig.legend(legend)
    if len(xticks)>0:
        fig.set_xticks(xticks+width-0.1)
        fig.set_xticklabels(xticklabels)

def draw_bars_chart(groups=[],width=0.1,color=[],ylabel='',xlabel='',xticks=[],xticklabels=(),figno=1,yerr=None,legend=None,title=''):
    figo=plt.figure(figno)
    fig=figo.add_subplot(111)
    ngrps=len(groups)
    index=np.arange(len(groups[0]))
    w=0
    rects=[]    
    for i in range(ngrps):
        print groups[i]
        rc=fig.bar(index+w,tuple(groups[i]),width=width,color=color[i],yerr=tuple(yerr[i]))
        rects.append(rc)
        w+=width
    fig.set_ylabel(ylabel)
    fig.set_xlabel(xlabel)
    fig.set_title(title)
    if len(xticks)>0:
        fig.set_xticks(xticks+width+0.05)
        fig.set_xticklabels(xticklabels)
    fig.legend([rect[0] for rect in rects],legend)


def demo_gender(participants=None,figno=1):
    n_male=0
    n_female=0
    for p in participants.values():
        if p.survey.gender.lower()=='male':
            n_male+=1
        else:
            if p.survey.gender.lower()=='female':
                n_female+=1
    
    labels='male','female'
    colors='r','b'
    fracs=[float(n_male)/(n_male+n_female)*100,float(n_female)/(n_male+n_female)*100]
    draw_pie_chart(fracs,labels=labels,colors=colors,figno=figno)
    

def demo_age(participants=None,figno=1):
    
    ages={}
    for p in participants.values():
        if not p.survey.age in ages.keys():
            ages[p.survey.age]=1
        else:
            ages[p.survey.age]+=1

    #sort a dictionary
    age_k=[]
    age_v=[]
    for key in sorted(ages.iterkeys()):
        age_k.append(key)
        age_v.append(ages[key])
    index=np.arange(len(ages.keys()))
    print index
    print tuple(age_k)
    draw_bar_chart(index,age_v,xticks=index,xticklabels=tuple(age_k),figno=figno)
    
    


def demo_nationality(participants=None,figno=1):
    print len(participants)
    natio={'Latin America':0.0,'UK':0.0,'Europe':0.0,'North America':0.0,'Asia':0.0,'Africa':0.0,'Australia':0.0,'Other':0.0}
    euroup=['Spain,http://www.farsnews.com/newstext.php?nn=13911022000293France','Italy','Germany','Other European Country']
    north_america=['United States','Other North American Country']
    for p in participants.values():
        if p.survey.nationality in euroup:
            natio['Europe']+=1
        if p.survey.nationality=='United Kingdom':
            natio['UK']+=1
        if p.survey.nationality in north_america:
            natio['North America']+=1
        if p.survey.nationality=='Asia':
            natio['Asia']+=1
        if p.survey.nationality=='Africa':
            natio['Africa']+=1
        if p.survey.nationality=='Other':
            natio['Other']+=1
        if p.survey.nationality=='Latin America':
            natio['Latin America']+=1
        if p.survey.nationality=='Australia':
            natio['Australia']+=1  

    empty_region=[]
    for key,item in natio.iteritems():
        if item==0:
            empty_region.append(key)
    if len(empty_region)>0:
        for i in range(len(empty_region)):
            natio.pop(empty_region[i])
    #sort a dictionary
    natio_k=[]
    natio_v=[]
    for key in sorted(natio.iterkeys()):
        natio_k.append(key)
        natio_v.append(natio[key])
    popul=sum(natio_v)
    natio_v=[ v/popul*100 for v in natio_v]
    colors=None
    colr='r','g','b','y','m','c','w'
    if len(natio_v)<=7:
        colors=colr[0:len(natio_v)]
    
    draw_pie_chart(data=natio_v,labels=tuple(natio_k),autopct='%1.1f%%',colors=colors,figno=figno)
    

def demo_following_BiSections(participants=None,figno=1,deloption=False,delindex=None):
    
    data=[]
    for p in participants.values():
        ans=p.survey.answers[0]
        ans=[int(i) for i in ans]
        #Cauuution
        if deloption==True and delindex!=None:
            del(ans[delindex])
        #Cauuution
        ans=[i/(float(sum(ans))) for i in ans]
        data.append(ans)
    data=np.matrix(data)
    mean_scores=np.mean(data,0)
    mean_scores= np.array(mean_scores)[0].tolist()
    p_personal=sum([mean_scores[0],mean_scores[1],mean_scores[4]])*100.0
    p_social=sum([mean_scores[2],mean_scores[3],mean_scores[5]])*100.0
    p_other=mean_scores[6]*100
    labels='Social Influence','Personal Interests','Other'
    colors='r','b','g'
    draw_pie_chart(data=[p_social,p_personal,p_other],labels=labels,colors=colors,figno=figno)
    #plt.title(bbox={'facecolor':'0.9', 'pad':5})
    
def demo_stop_following_BiSections(participants=None,figno=1,deloption=False,delindex=None):
    data=[]
    for p in participants.values():
        ans=p.survey.answers[1]
        ans=[int(i) for i in ans]
        #Cauuution
        if deloption==True and delindex!=None:
            del(ans[delindex])
        #Cauuution        
        ans=[i/(float(sum(ans))) for i in ans]
        data.append(ans)
    data=np.matrix(data)
    mean_scores=np.mean(data,0)
    mean_scores= np.array(mean_scores)[0].tolist()
    p_social=sum([mean_scores[2],mean_scores[3]])*100
    p_personal=sum([mean_scores[0],mean_scores[1]])*100.0
    p_other=mean_scores[4]*100.0
    labels='Social Influence','Personal Issues','Other'
    colors='r','b','g'
    draw_pie_chart(data=[p_social,p_personal,p_other],labels=labels,colors=colors,figno=figno)
    plt.title(' Population',bbox={'facecolor':'0.9', 'pad':5})

    
        
def demo_following_MultiSections(participants=None,figno=1):
    
    data=[]
    for p in participants.values():
        ans=p.survey.answers[0]
        ans=[int(i) for i in ans]
        ans=[i/(float(sum(ans))) for i in ans]
        data.append(ans)
    data=np.matrix(data)
    mean_scores=np.mean(data,0)
    sdev_scores=np.var(data,0)
    mean_scores= np.array(mean_scores)[0].tolist()
    sdev_scores= np.array(sdev_scores)[0].tolist()
    p_conform_frind=mean_scores[2]*100
    p_conform_crowd=mean_scores[4]*100
    p_reciprocity=mean_scores[3]*100
    p_identification=mean_scores[6]*100
    
    sdev_scores=(sdev_scores[2],sdev_scores[4],sdev_scores[3],sdev_scores[6])
    sdev_scores=[np.sqrt(i)*100 for i in sdev_scores]
    
    labels='Conform to Friends','Conform to Crowd','Reciprocity','Identification'
    #colors='r','b','y','g'
    values=[p_conform_frind,p_conform_crowd,p_reciprocity,p_identification]
    index=np.arange(len(values))
    draw_bar_chart(index,values,xticks=index,xticklabels=tuple(labels),color='g',ylabel='%',xlabel='Social Influence',figno=figno,yerr=sdev_scores)


def demo_stop_following_MultiSections(participants=None,figno=1):
    data=[]
    for p in participants.values():
        ans=p.survey.answers[1]
        ans=[int(i) for i in ans]
        ans=[i/(float(sum(ans))) for i in ans]
        data.append(ans)
    data=np.matrix(data)
    mean_scores=np.mean(data,0)
    sdev_scores=np.var(data,0)
    mean_scores= np.array(mean_scores)[0].tolist()
    sdev_scores= np.array(sdev_scores)[0].tolist()
    p_conformity=mean_scores[3]*100
    p_reactance=mean_scores[2]*100
    p_reciprocity=mean_scores[4]*100


    sdev_scores=(sdev_scores[3],sdev_scores[2],sdev_scores[4])
    sdev_scores=[np.sqrt(i)*100 for i in sdev_scores]
    
    labels='Conformity','Reactance','Reciprocity'
    values=[p_conformity,p_reactance,p_reciprocity]
    index=np.arange(len(values))
    draw_bar_chart(index,values,xticks=index,xticklabels=tuple(labels),color='g',ylabel='%',xlabel='Social Influence',figno=figno,yerr=sdev_scores) 
    #draw_pie_chart(data=values,labels=labels,colors=colors,figno=figno)



def demo_groups_survey_analysis(groups=[],ques_index=[],title="",legends=[],labels=[],options_index=[]):
    ##this functions recieves groups of participants, categorized based on a demographic, and then compare them based on specific questions and options indexed by  ques_index and option_index
    ##e.g. ques_index=[0,1] means that groups are compared based on the first and the second questions
    ##e.g. option_index=[[[1,3],[0,2]],[[1],[2]]] means that (i) in the first question the rates of option 1&3 are added up, also the rates of options 0&2 are added up and compared together with the options 1&2 of the second question.
    ## across_questions: if True the analysis is done for several questions
    ngroups=len(groups)
    data=[]
    data_sdev=[]
    for grp in range(ngroups):
        data.append([])
        data_sdev.append([])
        c=0
        for qus in ques_index:
            rates=[]
            for part in groups[grp].values():
                ans=part.survey.answers[qus]
                ans=normalize_rates(ans)
                ans=np.array(ans)
                p_rates=[]
                for optindx in options_index[c]:
                    p_rates.append(np.sum(ans[optindx]))
                rates.append(p_rates)
            avg_rate=np.median(np.matrix(rates),0).tolist()[0]
            sdev_rate=np.sqrt(np.var(np.matrix(rates),0)).tolist()[0]
            data[grp]+=avg_rate
            data_sdev[grp]+=sdev_rate
            c+=1
    print data
    colors='r','g','b','y','m','c','w'
    xticks=np.arange(len(data[0]))
    draw_bars_chart(data,color=colors,xlabel='Influence',xticklabels=labels,figno=1,yerr=data_sdev,legends=legends,xticks=xticks,title=title)


def demo_groups_twitter_analysis(groups=[],case=1,title="Twitter Data",legend=[],labels=[],fig=1):
    ngroups=len(groups)
    data=[]
    data_sdev=[]
    for grp in range(ngroups):
        data.append([])
        data_sdev.append([])
        for part in groups[grp].values():
            if part.stats!=None:
                if case==1 and part.stats.following_back_prop!=None:
                    data[grp].append(part.stats.following_back_prop)
                if case==2 and part.stats.common_followers_friends!=None:
                    data[grp].append(part.stats.common_followers_friends)
                if case== 3 and part.stats.n_followers!=None:
                    data[grp].append(part.stats.n_followers)
                if case== 4 and part.stats.n_friends!=None:
                    data[grp].append(part.stats.n_friends)
                if case== 5 and part.stats.n_tweets!=None:
                    data[grp].append(part.stats.n_tweets)
                    
        data_sdev[grp]=np.std(data[grp])
        data[grp]=np.median(data[grp])

    colors='r','g','b','y','m','c','w'
    index=range(0,len(data))
    xticks=np.arange(0,len(legend))
    xticklabels=tuple(legend)
    draw_bar_chart(index=index,values=data,width=0.35,color='k',ylabel='Frequency',xlabel='Ages',figno=fig,title=title,xticks=xticks,xticklabels=xticklabels)#,yerr=[]

def demo_twitter_correlation(participants=None,state=1,figno=1):
    X=[]
    Y=[]
    xlabel=None
    ylabel=None
    max_tweet=2000
    max_follow=1000
    max_friend=1000
    min_tweet=100
    min_follow=10
    min_friend=100 

    for participant in participants.values():
        if participant.stats!=None:
            if state==1 and participant.stats.n_tweets!=None and participant.stats.n_followers!=None:
##                if (participant.stats.n_tweets>max_tweet or participant.stats.n_followers>max_follow) or (participant.stats.n_tweets<min_tweet or participant.stats.n_followers<min_follow):
##                    continue
                X+=[participant.stats.n_tweets]
                Y+=[participant.stats.n_followers]
                xlabel='nTweets'
                ylabel='nFollowers'

            if state==2 and participant.stats.n_friends!=None and participant.stats.n_followers!=None:
##                if (participant.stats.n_friends>max_friend or participant.stats.n_followers>max_follow) or (participant.stats.n_friends<min_friend or participant.stats.n_followers<min_follow):
##                    continue
                X+=[participant.stats.n_friends]
                Y+=[participant.stats.n_followers]
                xlabel='nFriends'
                ylabel='nFollowers'

            if state==3 and participant.stats.n_friends!=None and participant.stats.n_tweets!=None:
##                if (participant.stats.n_friends>max_friend or participant.stats.n_tweets>max_tweet) or (participant.stats.n_friends<min_friend or participant.stats.n_tweets<min_tweet):
##                    continue
                X+=[participant.stats.n_tweets]
                Y+=[participant.stats.n_friends]
                xlabel='nTweets'
                ylabel='nFriends'

    draw_scatter_chart(X=X,Y=Y,xlabel=xlabel,ylabel=ylabel,figno=figno)


def demo_Big_twitter_correlation(state=1,figno=1): #similar to twitter but uses a large sample of twitter users' (participants+ their friends) to calculate a correlation
    X=[]
    Y=[]
    xlabel=None
    ylabel=None
    max_tweet=20000000#[100000,200000,200000]
    max_follow=200000
    max_friend=200000
    min_tweet=100
    min_follow=100
    min_friend=300 

    file_path='DataFiles/Users/usersDB1'
    if os.path.exists(file_path):
        with open(file_path,'rb') as handle:
            data=cpik.loads(handle.read())
    print len(data)
    for user in data.values():
        try:
            if state==1:
                if (user['statuses_count']>max_tweet or user['followers_count']>max_follow) or (user['statuses_count']<min_tweet or user['followers_count']<min_follow):
                    continue                
                X+=[user['statuses_count']]
                Y+=[user['followers_count']]
                xlabel='nTweets'
                ylabel='nFollowers'
            if state==2:
                if (user['friends_count']>max_friend or user['followers_count']>max_follow) or (user['friends_count']<min_friend or user['followers_count']<min_follow):
                    continue                                
                X+=[user['friends_count']]
                Y+=[user['followers_count']]
                xlabel='Number of Friends'
                ylabel='Number of Followers'
##                if user['followers_count']> 400000 and user['friends_count']>200000:
##                    print user['screen_name']               
            if state==3:
                if (user['statuses_count']>max_tweet or user['friends_count']>max_friend) or (user['statuses_count']<min_tweet or user['friends_count']<min_friend):
                    continue                               
                X+=[user['statuses_count']]
                Y+=[user['friends_count']]
                xlabel='nTweets'
                ylabel='nFriends'
        except Exception, ex:
            print ex.message
            continue
    draw_scatter_chart(X=X,Y=Y,xlabel=xlabel,ylabel=ylabel,figno=figno)

def demo_reciprocity_correl(participants):  
    surv_scores=[]
    twitter_scores=[]
    ques_index=0
    opt_index=0
    for key,participant in participants.iteritems():
        if participant.stats!=None and participant.stats.following_back_prop!=None:
            twitter_scores.append(participant.stats.following_back_prop)
            ans=participant.survey.answers[ques_index]
            ans=normalize_rates(ans)
            surv_scores.append(ans[opt_index])
    draw_scatter_chart(X=surv_scores,Y=twitter_scores,xlabel='Survey Data',ylabel='Twitter Data')


def draw_scatter_chart(X=[],Y=[],color='b',marker='o',xlabel='Twitter Data',ylabel='Survey Data',figno=1):
    figo=plt.figure(figno)
    plt.scatter(X,Y)
    fig=figo.add_subplot(111)
    fig.set_xlabel(xlabel)
    fig.set_ylabel(ylabel)
    rho=np.corrcoef(X,Y)[0][1]
    fig.set_title('correlation: '+str(rho))


def normalize_rates(ans=[]):
    ans=[int(i) for i in ans]
    ans=[i/(float(sum(ans))) for i in ans]
    return ans


##def demo_retweet_BiSections(participants=None,figno=1):
##    data=[]
##    for p in participants.values():
##        ans=p.survey.answers[2]
##        ans=[int(i) for i in ans]
##        ans=[i/(float(sum(ans))) for i in ans]
##        data.append(ans)
##    data=np.matrix(data)
##    mean_scores=np.mean(data,0)
##    mean_scores= np.array(mean_scores)[0].tolist()
##    p_social=sum(mean_scores[0:4])*100
##    p_personal=sum(mean_scores[4:6])*100.0
##    labels='Social Factors','Personal Factors'
##    colors='r','b'
##    draw_pie_chart(data=[p_social,p_personal],labels=labels,colors=colors,figno=figno)


def filter_date(path="DataFiles/stat_data.txt",age=set(['20 or younger','21-35','36-45','46-55','56-65','66 or older']),gender=set(['Male','Female']),nationality=set(['United Kingdom','France','Germany','Spain','Italy','Other European Country','United States','Other North American Country','Latin America','Asia','Australia','Africa','Other'])):
    #age, gender and nationality must be defined as sets
    participants=read_stat_data(path)
    filt_p={}
    for pkey,pitem in participants.iteritems():
        if pitem.survey.age in age and pitem.survey.gender in gender and pitem.survey.nationality in nationality:
            filt_p[pkey]=pitem
    return filt_p  

def calc_stats(stat_file_path='DataFiles/stat_data_2Q_rnd2.txt'):
    participants=read_stat_data(stat_file_path)
    path='DataFiles/participants/'
    #my_screen="data1_surgeon"
    #api=Auth.get_authentication(my_screen)  
    for key,participant in participants.iteritems():
        if participant.stats!=None:
            ID=participant.ID
            file_path=path+'followers_'+str(ID)
            followers,friends={},{}
            
            if os.path.exists (file_path):
                with open(file_path,'rb') as handle:
                    followers=cpik.loads(handle.read())
            else:
                continueStratagem
            file_path=path+'friends_'+str(ID)
            if os.path.exists (file_path):
                with open(file_path,'rb') as handle:
                    friends=cpik.loads(handle.read())
            else:
                continue
            common_memb=set.intersection (set(followers.keys()),set(friends.keys()))
            if len(followers)>0:
                participant.stats.following_back_prop=float(len(common_memb))/len(followers)
            else:
                print str(ID)+' has no follower!'
                participant.stats.following_back_prop=0
            if len(friends)>0:
                participant.stats.followed_back_prop=float(len(common_memb))/len(friends)
            else:
                print str(ID)+' has no friend!'
                participant.stats.followed_back_prop=0
            if len(followers)+len(friends)>0:
                participant.stats.common_followers_friends=float(len(common_memb))/(len(friends)+len(followers))

##            for friend in friends.keys():
##                usr=api.GetUser(friend)
##                participant.stats.friends_followers[frStratagemiend]=usr.GetFollowersCount()
##                participant.stats.friends_friends[friend]=usr.GetFriendsCount ()
##            
##            for follower in followers.keys():
##                usr=api.GetUser(follower)
##                participant.stats.followers_followers[follower]=usr.GetFollowersCount()
##                participant.stats.followers_friends[follower]=usr.GetFriendsCount ()
            participants[key]=participant

    write_stat_data(participants,out_path=stat_file_path)
            



font = {'family' : 'normal','weight' : 'bold','size'   : 28}
matplotlib.rc('font', **font)
out_path="DataFiles/stat_data_2Q_rnd2.txt"
#out_path1="DataFiles/stat_data.txt"
gender=set(['Male','Female'])
gender1=set(['Male'])
gender2=set(['Female'])
age=set(['20 or younger','21-35','36-45','46-55','56-65','66 or older'])
age1=set(['20 or younger'])
age2=set(['21-35'])
age3=set(['36-45'])
age4=set(['46-55','56-65','66 or older'])
age5=set(['56-65','66 or older'])
nationality=set(['United Kingdom','France','Germany','Spain','Italy','Other European Country','United States','Other North American Country','Latin America','Asia','Australia','Africa','Other'])
nationality1=set(['United Kingdom'])#,'Spain','Italy','Other European Country','France,Germany'
nationality2=set(['France','Germany'])#,'Other North American Country','Latin America'
nationality3=set(['Asia'])
nationality4=set(['Africa'])

#get_stats(in_path="Results/integerated_2q_rnd2.csv",out_path="DataFiles/stat_data_2Q_rnd2.txt")
participants1=filter_date(path=out_path,age=age1,gender=gender,nationality=nationality)
participants2=filter_date(path=out_path,age=age2,gender=gender,nationality=nationality)
participants3=filter_date(path=out_path,age=age3,gender=gender,nationality=nationality)
participants4=filter_date(path=out_path,age=age4,gender=gender,nationality=nationality)
participants5=filter_date(path=out_path,age=age5,gender=gender,nationality=nationality)
participants=filter_date(path=out_path,age=age,gender=gender,nationality=nationality)
#participants4=filter_date(path=out_path,age=age4,gender=gender,nationality=nationality)
#participants3=filter_date(path=out_path,age=age,gender=gender,nationality=nationality)
groups=[participants1,participants2,participants3,participants4]#participants5


legends=['Teen','Young','Adult','Aged']#,'Adult','Aged','Old'
#demo_following_BiSections(participants=participants,figno=2,deloption=True,delindex=4)
#demo_stop_following_BiSections(participants=participants,figno=2,deloption=True,delindex=3)
#demo_retweet_BiSections()
#demo_following_MultiSections(participants=participants,figno=1)      
#demo_stop_following_MultiSections(participants=participants,figno=2)

#demo_age(participants=participants,figno=1)

#demo_groups_survey_analysis(groups,ques_index=[[2],[3]],title="Conformity",legends=['UK','Europe','NorthAmerica','Asia','Other'],labels=['following','stop following'])
#demo_groups_survey_analysis(groups,ques_index=[3,4],title="Reciprocity",legends=legends,labels=['following','stop following'])
#demo_groups_survey_analysis(groups,ques_index=[6,-1],title="Identification",legends=legends,labels=['following','stop following'])
#demo_groups_survey_analysis(groups,ques_index=[-1,2],title="Reactance",legends=legends,labels=['stop following','stop following'])

#demo_groups_survey_analysis(groups,ques_index=[0],title="Social",options_index=[[[0,1,4]],[[0,1,3],[2,4,5],[6]]],legends=legends,labels=['Social Factors','Conformity','Reactance'])

##lbl='Age Group'
##demo_groups_twitter_analysis(groups,case=2,title="Commonality",labels=[lbl],fig=1,legend=legends)
##demo_groups_twitter_analysis(groups,case=3,title="Followers",labels=[lbl],fig=2,legend=legends)
##demo_groups_twitter_analysis(groups,case=4,title="Following",labels=[lbl],fig=3,legend=legends)
##demo_groups_twitter_analysis(groups,case=5,title="Tweets",labels=[lbl],fig=4,legend=legends)

#calc_stats()
#participants=read_stat_data()
##demo_reciprocity_correl(participants1)

##demo_twitter_correlation(participants=participants,state=1,figno=1)
##demo_twitter_correlation(participants=participants,state=2,figno=2)
##demo_twitter_correlation(participants=participants,state=3,figno=3)

#demo_Big_twitter_correlation(state=1,figno=1)
demo_Big_twitter_correlation(state=2,figno=2)
#demo_Big_twitter_correlation(state=3,figno=3)


plt.show()

