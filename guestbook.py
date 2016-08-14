'''
Guestbook Parser

Guestbook analyzes an Apache log file and returns information about who 
visited a site, or a particular part of a site. For example, it can be used
to retrieve information about visitors' geographic location, or the most frequent
visitors by IP address. 

It uses the freegeoip.net location API. 
	

******************************************************************
USAGE
******************************************************************
python ApacheLogParser.py [Access log location] [Optional Parameters]

******************************************************************
OPTIONAL PARAMETERS
******************************************************************
- request [substring]			Returns all matches with this substring in the request
- count							Returns the most common IP addresses for visitors
- track							Also displays geolocation information about IP address


'''

from models.Visitor import Visitor

a = Visitor()