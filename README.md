UCAMB_SocialInfluence
=====================

One of the main tasks of UCAMB in the Recognition project is to understand decision making process in micro scale with a focus on psychological aspects and their impacts on a social network's dynamic. Therefore, our experiments and analysis aim at extracting various social traits of human behaviour and grouping common behaviours in a social network. Specifically, we aim at understanding the nature and causes of a person's behaviour in a social network. Further, we identify the factors that lead an individual to behave in a given way in the presence of others, and look at the conditions under which certain behaviour/decision occurs. The source codes pushed here are used for the associated experiments.

twitter.py:
A Python wrapper around the Twitter API. This module provides a pure Python interface for the Twitter API. Twitter provides a service that allows people to connect via the web, IM, and SMS. Twitter exposes a web services API (http://dev.twitter.com/doc) and this module is intended to make it even easier for Python programmers to use. Further information about this module is available on https://code.google.com/p/python-twitter/.

Auth.py:
Twitter supports a few authentication methods and with a range of OAuth authentication styles. You are supposed to know which authentication method you need to use. To learn about Twitter authentication methods you should read on https://dev.twitter.com/docs/auth.  When choosing which authentication method to use you should understand the way that method will affect your users experience and the way you write your application. 
To use authentication method you need to set your (i) consumer key (ii) consumer secret (iii) access token key and (iv)access token secret, in Auth.py.

