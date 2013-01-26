import twitter
import urllib2
from sets import Set

#data1_surgeon
con_key='95xlaFoKBsebx6dVUh9WSw'
con_sec='ERNTKp0m1SvaXi3Y6NIF97JKIp4pn2DiTOvR3vVGR1U'
acc_tok='897433675-1EdKl4xnaxImIG2uf95CXoH25xGfIEfO5H7GxRz4'
acc_sec='lqXp0hPX5FkKQPych8mAbPNE1tm6Gfj2LuCdGyaViM'

#mehdy_h59
##con_key='49Jf6XcYS6nFfDAnD8OxA'
##con_sec='Ny7hLvcGNCfafcJykkPpFED350BQ0JjrweOJcVsJs'
##acc_tok='34409944-kRuM7yKAqsAR1x7PROK6PPH0VWdIKu3ds4cIV8Oz0'
##acc_sec='jX2ZwxgkV3pg3M8z2FAfoQ50zIgvLnrw2frLVbr9E'



api=twitter.Api(consumer_key=con_key,consumer_secret=con_sec,access_token_key=acc_tok,access_token_secret=acc_sec)
#print api.VerifyCredentials()
following = []
cursor = -1
##while cursor!=0:
##    ret = api.GetFriends(cursor=cursor)
##    following += ret["users"]
##    #[following.append(twitter.User.NewFromJsonDict(x)) for x in ret["users"]]
##    cursor=ret["next_cursor"]
##    #print cursor;
##
##print len(following);

num=50
i=1
screen_name="mehdy_h59"
#text="1 miniute Twitter survey run by researchers @ ComputerLab Cambridge University. Please help us by answering 4 questions "
text="1 miniute Twitter survey run by researchers @ ComputerLab Cambridge University. Your contribution will be appreciated! "
url="www.cl.cam.ac.uk/~mh717/survey_Twitter/intro.html?esm="
usr=api.GetUser(screen_name);
usrID=list(str(usr.GetId()));
usrID.reverse();
usrID="".join(usrID);
url+=usrID;
url=urllib2.quote(url.encode("utf8"))
text+=url;
print text
api.PostDirectMessage(screen_name,text)

#for friend in following:
    #print friend.screen_name;
#api.CreateFriendship('mehdy_h59');

