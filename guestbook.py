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
import sys
import re
from models.Visitor import Visitor
from models.Visit import Visit

visitsList = []
visitorsList = {}

regexString = '(\S+) (\S+) (\S+) \[([^:]+):(\d+:\d+:\d+) ([^\]]+)\] \"(\S+) (.*?) (\S+)\" (\S+) (\S+) "([^"]*)" "([^"]*)"'

def main(args):
	if (len(args) < 2):
		print "Not enough arguments! See usage"
		return -2

	fileLocation = args[1]
	
	importVisitsFromFile(fileLocation)

# Populate visits list from access log
def importVisitsFromFile(fileLocation):
	compiledRegex = re.compile(regexString)

	with open(fileLocation) as f:
	    for line in f:
	    	result = compiledRegex.match(line)

	    	if result:
		    	result = result.groups()
		    	ip = result[0]
		    	domain = result[11]
		    	page = result[7]
		    	dateTime = result[3] + " " + result[4]
		    	userAgent = result[12]

		    	_visit = Visit(ip, domain, page, dateTime, userAgent)
		    	print(_visit)

		    	visitsList.append(_visit)



if __name__ == "__main__":
    main(sys.argv)