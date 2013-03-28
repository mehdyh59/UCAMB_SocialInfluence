import twitter
import urllib2
from sets import Set

api=twitter.Api(consumer_key=con_key,consumer_secret=con_sec,access_token_key=acc_tok,access_token_secret=acc_sec)
following = []
cursor = -1


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


