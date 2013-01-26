import twitter
from sets import Set

#data1_surgeon
con_key='95xlaFoKBsebx6dVUh9WSw'
con_sec='ERNTKp0m1SvaXi3Y6NIF97JKIp4pn2DiTOvR3vVGR1U'
acc_tok='897433675-1EdKl4xnaxImIG2uf95CXoH25xGfIEfO5H7GxRz4'
acc_sec='lqXp0hPX5FkKQPych8mAbPNE1tm6Gfj2LuCdGyaViM'

#mehdy_h59
#con_key='49Jf6XcYS6nFfDAnD8OxA'
#con_sec='Ny7hLvcGNCfafcJykkPpFED350BQ0JjrweOJcVsJs'
#acc_tok='34409944-kRuM7yKAqsAR1x7PROK6PPH0VWdIKu3ds4cIV8Oz0'
#acc_sec='jX2ZwxgkV3pg3M8z2FAfoQ50zIgvLnrw2frLVbr9E'


api=twitter.Api(consumer_key=con_key,consumer_secret=con_sec,access_token_key=acc_tok,access_token_secret=acc_sec)
##followers = []
##cursor = -1
##while cursor!=0:
##    ret = api.GetFollowers(cursor=cursor)
##    followers += ret["users"]
##    cursor=ret["next_cursor"]




num=50
i=1
text="Hi, researchers in the computer lab of Cambridge university are running a survey on Twitter. Please help us by filling our onlt one page questionnair http://www.cl.cam.ac.uk/~mh717/survey_Twitter/intro.html"
api.PostDirectMessage('mehdy_h59',text)
#for follower in followers:
    #i++;
    #friend.screen_name;
    
#api.CreateFriendship('mehdy_h59');

