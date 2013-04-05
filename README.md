UCAMB_SocialInfluence
=====================

One of the main tasks of UCAMB in the Recognition project is to understand decision making process in micro scale with a focus on psychological aspects and their impacts on a social network's dynamic. Therefore, our experiments and analysis aim at extracting various social traits of human behaviour and grouping common behaviours in a social network. Specifically, we aim at understanding the nature and causes of a person's behaviour in a social network. Further, we identify the factors that lead an individual to behave in a given way in the presence of others, and look at the conditions under which certain behaviour/decision occurs. This source codes repository is used for the associated experiments.

twitter.py:
A Python wrapper around the Twitter API. This module provides a pure Python interface for the Twitter API. Twitter exposes a web service API (http://dev.twitter.com/doc) and this module is intended to make it even easier for Python programmers to use. Further information about this module is available on https://code.google.com/p/python-twitter/.

Auth.py:
Twitter supports a few authentication methods with a range of OAuth authentication styles. You are supposed to know which authentication method you need to use. To learn about Twitter authentication methods you should read on https://dev.twitter.com/docs/auth.  When choosing which authentication method to use you should understand the way that method will affect your users experience and the way you write your application. 
To use authentication methods you need to set your (i) consumer key (ii) consumer secret (iii) access token key and (iv)access token secret, in Auth.py. All of it is done after you sign up in Twitter as a developer and register your application on https://dev.twitter.com/.

Invitations.py:
This module samples a subset, say m (m is 250 by default), of followers of an authorized account, and send them an invitation message on Twitter to ask them to fill the questionnaire. The length of invitation message should no exceed the Twitter's limit which at the moment is 140 characters. This module samples the followers randomly. However, it also has the advantage to filter followers based on the date of following.


Participants_Graph.py:
This module regularly checks the graph associated with each participant, a twitter user who participated in our questionnaire, and record those links recently added/removed from the graph, e.g. it monitors new followers and new followees of the participant as well as former followers/followees who are not any longer in relationship with the participant. The output of this module can be used to represent the dynamic of the participants graph.

Following.py:
this module lets an authenticated user automatically follows an individual or a group of individuals at the same time. A set of conditions, e.g. number of followers, number of tweets, number of followees etc, are also defined based on which individuals are followed. For instance, it can sample from thoes followers who started to follow a user after 20th Feb 2013.

Stop_Following.py:
this module lets an authenticated user automatically stop following an individual or a group of users at the same time. Some conditions are defined based on which unfollowing function performs.

stats.py:
this module does some data analysis based on the data collected from participants. This module makes use of data collected by the questionnaire as well as data crawled in Twitter to compute various statistics and draw summary charts. This module uses matplotlib.py, will be introduced shortly, library for drawing plots.

matplotlib.py:
is a python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms. Further information is available on http://matplotlib.org/.

 update_followers.py:
 The list of followers of a particular participant may vary time to time. This module is used to regularly update the list of followers of a particular participants. 
 
 update_friends.py:
 The list of friends of a particular participant may vary time to time. This module is used to regularly update the list of friends of a particular participants. 
 
 
 
 
 
 
 

