UCAMB_SocialInfluence
=====================

One of the main tasks of UCAMB in the Recognition project is to understand decision making process in micro scale with a focus on psychological aspects and their impacts on a social network's dynamic. Therefore, our experiments and analysis aim at extracting various social traits of human behaviour and grouping common behaviours in a social network. Specifically, we aim at understanding the nature and causes of a person's behaviour in a social network. Further, we identify the factors that lead an individual to behave in a given way in the presence of others, and look at the conditions under which certain behaviour/decision occurs. These source codes repository is used for the associated experiments.



Modules:

Auth.py:
Twitter supports a few authentication methods with a range of OAuth authentication styles. You are supposed to know which authentication method you need to use. To learn about Twitter authentication methods you should read on https://dev.twitter.com/docs/auth.  When choosing which authentication method to use you should understand the way that method will affect your users experience and the way you write your application. 
To use authentication methods you need to set your (i) consumer key (ii) consumer secret (iii) access token key and (iv)access token secret, in Auth.py, All of which can be obtained once you sign up in Twitter as a developer and register your application on https://dev.twitter.com/.

Following.py:
this module lets an authenticated user automatically follows an individual or a group of individuals at the same time. A set of conditions, e.g. number of followers, number of tweets, number of followees etc, are also defined based on which individuals are followed. For instance, it can sample from thoes followers who started to follow a user after 20th Feb 2013.

Stop_Following.py:
this module lets an authenticated user automatically stop following an individual or a group of users at the same time. Some conditions are defined based on which unfollowing function performs. For instance, you can stop following those users who have not been an active user for a long time. The activity is defined based on the number of following/followed as well as tweetings/re-tweeting actions.

UserInfo_scrape.py:
this module scrapes profile information from a particular participant or a group of participants and stores them on a local disk. It can capture all information about a user profile, e.g. screen name, ID, #tweets, #re-tweets, #followers, #friends, etc. At the moment, it only records #followers, #friends and #tweets and threws away the rest of info due to lack of space. However, with some minor changes in code, one can store all the information available in a user's profile. To cope with downloading limits imposed by Twitter several authenticated users can be used at the same time to collect required data. Also, the parallel python library (http://www.parallelpython.com/) is used to speed up the scraping process.

Tweets_scrape.py:
this module scrapes tweets from a particular participants or a group of participants and stores them on a local disk. It captures all information about a tweet, e.g. text, created_date, creator's ID, creator's screen name, whether or not it's retweeted, ... .

Invitations.py:
This module samples a subset, say m (m is 250 by default), of followers of an authorized account, and send them an invitation message on Twitter to ask them to fill the questionnaire. The length of invitation message should no exceed the Twitter's limit which at the moment is 140 characters. This module samples the followers randomly. However, it also has the advantage to filter followers based on the date of following.

Participants_Graph.py:
This module regularly checks the graph associated with each participant, a twitter user who participated in our questionnaire, and record those links recently added/removed from the graph, e.g. it monitors new followers and new followees of the participant as well as former followers/followees who are not any longer in relationship with the participant. The output of this module can be used to represent the dynamic of the participants graph.

update_friends.py:
The list of friends of a particular participant may vary time to time. This module is used to regularly monitor the list of current friends of a particular participants and record the fresh list of friends on a local disk.  This module is used by Participants_Graph.py.
  
update_followers.py:
The list of followers of a particular participant may vary time to time. This module is used to regularly monitor the list of current followers of a particular participants and record the on a local disk. This module is used by Participants_Graph.py. 

stats.py:
this module does some data analysis based on the data collected from participants. This module makes use of data collected by the questionnaire as well as data crawled in Twitter to compute various statistics and draw summary charts. This module uses matplotlib.py, will be introduced shortly, library for drawing plots.

Libraries:

twitter:
A Python wrapper around the Twitter API. This module provides a pure Python interface for the Twitter API. Twitter exposes a web service API (http://dev.twitter.com/doc) and this module is intended to make it even easier for Python programmers to use. Further information about this module is available on https://code.google.com/p/python-twitter/.

simplejson 3.1.2:
simplejson is a simple, fast, complete, correct and extensible JSON <http://json.org> encoder and decoder for Python 2.5+ and Python 3.3+. It is pure Python code with no dependencies, but includes an optional C extension for a serious speed boost. Read more on https://pypi.python.org/pypi/simplejson.

Httplib2:
A comprehensive HTTP client library that supports many features left out of other HTTP libraries for python. Read more on https://code.google.com/p/httplib2/.

oauth2:
a python wrapper around OAuth 2.0. Read the details on https://github.com/simplegeo/python-oauth2.  OAuth 2.0 is the next evolution of the OAuth protocol. OAuth 2.0 focuses on client developer simplicity while providing specific authorization flows for web applications, desktop applications, mobile phones, and living room devices. This specification is being developed within the IETF OAuth WG and is based on the OAuth WRAP proposal. 

matplotlib:
is a python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms. Further information is available on http://matplotlib.org/.

nltk:
NLTK is a python library for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning. You can read more on http://nltk.org/.

parallel python (PP):
PP is a python module which provides mechanism for parallel execution of python code on SMP (systems with multiple processors or cores) and clusters (computers connected via network). Read more on http://www.parallelpython.com/ .
