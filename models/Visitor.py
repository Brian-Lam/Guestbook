'''
Visitor

This class represents a visitor to a web server - visitors are differentiated by IP address. Each visitor
will have a list of Visits attached to it, as well as a map to count their number of hits on each page
'''
import collections

class Visitor:

	def __init__(self, ipAddress=""):
		self.visits =  []
		self.ipAddress = ipAddress
		self.pages = collections.defaultdict(int)
		self.visitCount = 0
		self.userAgents = set()
		
	def addVisit(self, visit):
		self.visits.append(visit)
		self.visitCount += 1
		self.pages[visit.getFullUrl()] += 1
		self.userAgents.add(visit.userAgent)

	def pageBreakdown(self):
		result = ""
		for key, value in self.pages.iteritems():
			result += ("    {}: {} visits").format(key, value)
			result += "\n"
		return result
	
	def userAgentsString(self):
		result = ""
		for agent in self.userAgents:
			result += agent
			result += "\n"
		return result
