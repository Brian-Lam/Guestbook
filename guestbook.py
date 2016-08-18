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
guestbook.py [-h] [-agents AGENTS] [-times TIMES] [-cutoff [CUTOFF]]
                [-popular] [-track] [-breakdown] [-target TARGET]
                filePath

positional arguments:
  filePath          Filepath for access log

optional arguments:
  -h, --help        show this help message and exit
  -agents AGENTS    Show user agents for a given ip
  -times TIMES      Show page visits with timestamps for a particular IP
                    address
  -cutoff [CUTOFF]  Minimum view count cutoff when showing results
  -popular          Show IP addresses of most popular visits
  -track            Enable tracking IP geolocation. Results will be shown with
                    tracking data.
  -breakdown        Show page visit breakdown for each IP address
  -target TARGET    Only show results for this IP address
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

# Add command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filePath", type=str, help="Filepath for access log")
parser.add_argument("-agents", type=str, help="Show user agents for a given ip")
parser.add_argument("-times", type=str, help="Show page visits with timestamps for a particular IP address")
parser.add_argument("-cutoff", nargs="?", type=int, default=False, help="Minimum view count cutoff when showing results")
parser.add_argument("-popular", action="store_true", help="Show IP addresses of most popular visits")
parser.add_argument("-track", action="store_true", help="Enable tracking IP geolocation. Results will be shown with tracking data.")
parser.add_argument("-breakdown", action="store_true", help="Show page visit breakdown for each IP address")
parser.add_argument("-target", help="Only show results for this IP address")

def main(args):
	# Parse arguments
	args = parser.parse_args()

	fileLocation = args.filePath
	importVisitsFromFile(fileLocation)

	# Show known user agents for an IP address
	if (args.agents):
		showAgents(args.agents, args)

	# Show access times for an IP address
	if (args.times):
		showTimes(args.times, args)

	# Show the IP addresses with the most hits
	if (args.popular):
		mostPopularVisitors(args.track, args.cutoff)

	# List IP addresses of visitors and which pages they visited
	if (args.breakdown):
		visitorPages(args.target, args)

# Prints out information about the visitors with the highest page hits.
# Optional parameter: track
# If track is set to true, this script will also send out a request to freegeoip.net
# to retreive IP address geolocation information
def mostPopularVisitors(track=False, cutoff=None):
	for visitor in (sorted(visitorsMap.values(), key=operator.attrgetter('visitCount'), reverse=True)):
		# Hide results that have less views than the cutoff
		if cutoff:
			if visitor.visitCount < cutoff:
				continue

		# If geotracking has been enabled
		if track:
			# getGeoLocationDataString(visitor)
			print getGeoLocationDataString(visitor)

		print "{} - {} visits".format(visitor.ipAddress, visitor.visitCount)

		# Onle line break if we're also displaying geolocation data
		if track:
			print ""

# Prints out information about pages that a user has visited, and
# the pagehits on each page.
def visitorPages(targetIp=None, args=None):
	# Only print page breakdown for target visitor
	if targetIp:
		if targetIp in visitorsMap.keys():
			print visitorsMap[targetIp].pageBreakdown()
			return
		else:
			print "Could not find any records for this IP in the access log file"
	else:
		# If no target IP, print out page breakdown for all visitors
		for ip, visitor in visitorsMap.iteritems():
			print ip
			print visitor.pageBreakdown()

# Prints out information about the known user agents for a
# given IP address.
def showAgents(targetIp, args=None):
	if targetIp and targetIp in visitorsMap.keys():
		print visitorsMap[targetIp].userAgentsString()
	else:
		print "Could not find any records for this IP in the access log file"

# Prints out information about access times for a 
# given IP address.
def showTimes(targetIp, args=None):
	if targetIp and targetIp in visitorsMap.keys():
		visitor = visitorsMap[targetIp]
		print "\nShowing access times for {}\n".format(targetIp)
		if args and args.track:
			geoData = getGeoLocationDataString(visitor)
			print "{}\n".format(geoData)

		print visitor.timesAndUrls()
	else:
		print "Could not find any records for this IP in the access log file"

'''
*********************************************************************
Helper functions
*********************************************************************
'''

def getGeoLocationDataString(visitor):
	url = "http://freegeoip.net/json/{}".format(visitor.ipAddress)
	apiResponse = urllib2.urlopen(url)
	country, city, region_name, zip_code = parseGeoLocationData(apiResponse) or (None, None, None, None, None)

	return "{} {}, {}  {}".format(country, city, region_name, zip_code)

# Given an API response from freegeoip, parse it and return 
# geolocation data in a tuple
def parseGeoLocationData(apiResponse):
	userData = json.load(apiResponse)
	# Cleanse data and remove bad encoding
	country = userData["country_name"].encode('ascii', 'ignore')
	city = userData["city"].encode('ascii', 'ignore')
	region_name = userData["region_name"].encode('ascii', 'ignore')
	zip_code = userData["zip_code"].encode('ascii', 'ignore')
	return country, city, region_name, zip_code

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
				if ip not in visitorsMap:
					visitorsMap[ip] = Visitor(ip)

				visitorsMap[ip].addVisit(visit)

# Run if started from command line
if __name__ == "__main__":
	main(sys.argv)