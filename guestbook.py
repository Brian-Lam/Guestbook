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
import argparse
from models.Visitor import Visitor
from models.Visit import Visit


'''
*********************************************************************
SETUP
*********************************************************************
'''
# Store a list of all visits
visitsList = []
# Store visitors by IP
visitorsMap = {}
# Regex string to match 
regexString = '(\S+) (\S+) (\S+) \[([^:]+):(\d+:\d+:\d+) ([^\]]+)\] \"(\S+) (.*?) (\S+)\" (\S+) (\S+) "([^"]*)" "([^"]*)"'

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="Filepath for access log")
parser.add_argument("track", nargs="?", help="Enable tracking IP geolocation")
parser.add_argument("-cutoff", nargs="?", type=int, default=False, help="Minimum view count cutoff when showing results")


def main(args):
	# TODO: Argument parsing
	args = parser.parse_args()
	fileLocation = args.file
	importVisitsFromFile(fileLocation)

	enableTracking = (not args.track == None)

	# Show the IP addresses with the most hits
	mostPopularVisitors(args.track, args.cutoff)

	# List IP addresses of visitors and which pages they visited
	#visitorPages()

# Populate visits list from access log
def importVisitsFromFile(fileLocation):
	compiledRegex = re.compile(regexString)

	with open(fileLocation) as f:
	    for line in f:
	    	ip, domain, page, dateTime, userAgent = getInfoFromLogLine(compiledRegex, line) or (None, None, None, None, None)

	    	if ip:
		    	# Update visits list
		    	visit = Visit(ip, domain, page, dateTime, userAgent)
		    	visitsList.append(visit)

		    	# Update visitors hashmap
		    	if not ip in visitorsMap:
		    		visitorsMap[ip] = Visitor(ip)
		    	visitorsMap[ip].addVisit(visit)

# Extracts specific pieces of data from a line in the 
# access log. Returns None if no matches are found. 
def getInfoFromLogLine(compiledRegex, line):
	result = compiledRegex.match(line)

	if result is not None:
		result = result.groups()
	else: 
		return None

	if result is not None:
		ip = result[0]
		domain = result[11]
		page = result[7]
		dateTime = result[3] + " " + result[4]
		userAgent = result[12]

		return ip, domain, page, dateTime, userAgent

	return None

# Prints out information about the visitors with the highest page hits. 
# Optional parameter: track
# If track is set to true, this script will also send out a request to freegeoip.net
# to retreive IP address geolocation information
def mostPopularVisitors(track = False, cutoff = None):
	for visitor in (sorted(visitorsMap.values(), key=operator.attrgetter('visitCount'), reverse=True)):
		# Hide results that have less views than the cutoff
		if cutoff:
			if visitor.visitCount < cutoff:
				continue 

		# If geotracking has been enabled
		if track:
			url = "http://freegeoip.net/json/{}".format(visitor.ipAddress)
			apiResponse = urllib2.urlopen(url)
			country, city, region_name, zip_code = getGeoLocationData(apiResponse) or (None, None, None, None, None)

			userString = "{} {}, {}  {}".format(country, city, region_name, zip_code)
			print userString

		print "{} - {} visits".format(visitor.ipAddress, visitor.visitCount)
		print ""

# Given an API response from freegeoip, parse it and return 
# geolocation data in a tuple
def getGeoLocationData(apiResponse):
	userData = json.load(apiResponse)
	# Cleanse data and remove bad encoding
	country = userData["country_name"].encode('ascii', 'ignore')
	city = userData["city"].encode('ascii', 'ignore')
	region_name = userData["region_name"].encode('ascii', 'ignore')
	zip_code = userData["zip_code"].encode('ascii', 'ignore')
	return country, city, region_name, zip_code

# Prints out information about pages that a user has visited, and
# the pagehits on each page.
def visitorPages(targetIp = None):
	# Only print page breakdown for target visitor
	if targetIp and targetIp in visitorsMap.keys():
		print visitorsMap[targetIp].pageBreakdown
		return
	# If no target IP, print out page breakdown for all visitors
	for ip, visitor in visitorsMap.iteritems():
		print ip
		print visitor.pageBreakdown()

if __name__ == "__main__":
    main(sys.argv)