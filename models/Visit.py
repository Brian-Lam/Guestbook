'''
Visit 

This class represents a unique visit to a site, as logged in the access logs. Visitors will store a 
list of these visits. 
'''

class Visit:
	ipAddress = ""
	pageUrl = ""

	def __init__(self, ipAddress, domain, pageUrl="", dateTime="", userAgent=""):
		self.ipAddress = ipAddress
		self.domain = domain
		self.pageUrl = pageUrl
		self.dateTime = dateTime
		self.userAgent = userAgent
		self.fullUrl = self.domain + self.pageUrl

	def __str__(self):
		return "{} - {} {} - {} - {} ".format(self.ipAddress, self.domain, self.pageUrl, self.dateTime, self.userAgent[:50])
	
	def getFullUrl(self):
		return self.fullUrl.replace("//", "/")

	def getFullUrlAndTime(self):
		return "{}: {}".format(self.dateTime, self.getFullUrl())