UCAMB_SocialInfluence
=====================

One of the main tasks of UCAMB in the Recognition project is to understand decision making process in micro scale with a focus on psychological aspects and their impacts on a social network's dynamic. Therefore, our experiments and analysis aim at extracting various social traits of human behaviour and grouping common behaviours in a social network. Specifically, we aim at understanding the nature and causes of a person's behaviour in a social network. Further, we identify the factors that lead an individual to behave in a given way in the presence of others, and look at the conditions under which certain behaviour/decision occurs. The source codes pushed here are used for the associated experiments.

twitter.py:
A Python wrapper around the Twitter API. This module provides a pure Python interface for the Twitter API. Twitter provides a service that allows people to connect via the web, IM, and SMS. Twitter exposes a web services API (http://dev.twitter.com/doc) and this module is intended to make it even easier for Python programmers to use. Further information about this module is available on https://code.google.com/p/python-twitter/.

Auth.py:
Twitter supports a few authentication methods and with a range of OAuth authentication styles. You are supposed to know which authentication method you need to use. To learn about Twitter authentication methods you should read on https://dev.twitter.com/docs/auth.  When choosing which authentication method to use you should understand the way that method will affect your users experience and the way you write your application. 
To use authentication method you need to set your (i) consumer key (ii) consumer secret (iii) access token key and (iv)access token secret, in Auth.py.

Invitations.py:
This module samples a subset, say m (m is 250 by default), of followers of an authorized account, and send them an invitation message on Twitter to ask them to fill the questionnaire. The lenght of invitation message should no exceed the Twitter's limit which at the moment is 140 characters. This module samples the followers randomly. However, it also has the advantage to filter followers based on the date of following.


Participants_Graph.py:
This module regularly checks the graph associated with each participant, a twitter user who participated in our questionnaire, and record those links recntely added/removed from the graph, e.g. it monitors new followers and new followees of the participants as well as former followers/followees who are not any longer in relationship with the participant.

Following.py:
this module lets an authenticated user authomatically follows an individual or a group of individuals at the same time. A set of conditions, e.g. number of followers, number of tweets, number of followees etc, are also defined based on which individuals are followed.

Stop_Following.py:
this module lets an authenticated user authomatically stops following an individual or a group of users at the same time. Some conditions are defined based on which unfollowing function performs.

stats.py:
this module does some data analysis based on the data collected from participants. This module makes use of data collected by the questionnaire as well as data crawled in Twitter to compute various statistics and draw summary charts. This module uses matplotlib.py, will be introduced shortly, library for drawing plots.

matplotlib.py:
is a python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms. Further information is available on http://matplotlib.org/.



