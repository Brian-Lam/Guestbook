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
import operator
import re
import urllib2
import json
from models.Visitor import Visitor
from models.Visit import Visit

# Store a list of all visits
visitsList = []
# Store visitors by IP
visitorsMap = {}
# Regex string to match 
regexString = '(\S+) (\S+) (\S+) \[([^:]+):(\d+:\d+:\d+) ([^\]]+)\] \"(\S+) (.*?) (\S+)\" (\S+) (\S+) "([^"]*)" "([^"]*)"'

def main(args):
	if (len(args) < 2):
		print "Not enough arguments! See usage"
		return -2

	fileLocation = args[1]
	importVisitsFromFile(fileLocation)
	mostPopularVisitors(True)
	# visitorPages()

# Populate visits list from access log
def importVisitsFromFile(fileLocation):
	compiledRegex = re.compile(regexString)

	with open(fileLocation) as f:
	    for line in f:
	    	result = compiledRegex.match(line)

	    	if result:
		    	result = result.groups()
		    	# TODO: Can we fix these magic numbers?
		    	ip = result[0]
		    	domain = result[11]
		    	page = result[7]
		    	dateTime = result[3] + " " + result[4]
		    	userAgent = result[12]

		    	# Update visits list
		    	visit = Visit(ip, domain, page, dateTime, userAgent)
		    	visitsList.append(visit)

		    	# Update visitors hashmap
		    	if not ip in visitorsMap:
		    		visitorsMap[ip] = Visitor(ip)
		    	visitorsMap[ip].addVisit(visit)

# Prints out information about the visitors with the highest page hits. 
# Optional parameter: track
# If track is set to true, this script will also send out a request to freegeoip.net
# to retreive IP address geolocation information
def mostPopularVisitors(track = False):
	for visitor in (sorted(visitorsMap.values(), key=operator.attrgetter('visitCount'), reverse=True)):
		if track:
			url = "http://freegeoip.net/json/{}".format(visitor.ipAddress)
			apiResponse = urllib2.urlopen(url)
			userData = json.load(apiResponse)

			country = userData["country_name"].encode('ascii', 'ignore')
			city = userData["city"].encode('ascii', 'ignore')
			region_name = userData["region_name"].encode('ascii', 'ignore')
			zip_code = userData["zip_code"].encode('ascii', 'ignore')

			userString = "{} {}, {}  {}".format(country, city, region_name, zip_code)
			print "{} - {} visits".format(visitor.ipAddress, visitor.visitCount)
			print userString
			print ""
		else:
			print "{} - {} visits".format(visitor.ipAddress, visitor.visitCount)

# Prints out information about pages that a user has visited, and
# the pagehits on each page.
def visitorPages():
	for ip, visitor in visitorsMap.iteritems():
		print ip
		print visitor.pageBreakdown()

if __name__ == "__main__":
    main(sys.argv)