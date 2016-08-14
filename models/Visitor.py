import collections

class Visitor:
	ipAddress = ""
	location = ""
	visits =  []
	pages = collections.defaultdict(int)
	visitCount = 0

	def __init__(self, ipAddress=""):
		self.ipAddress = ipAddress
		
	def addVisit(self, visit):
		self.visits.append(visit)
		self.visitCount += 1
		self.pages[visit.getFullUrl()] += 1

	def pageBreakdown(self):
		result = ""
		for key, value in self.pages.iteritems():
			result += ("    {}: {} visits").format(key, value)
			result += "\n"
		return result