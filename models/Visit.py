class Visit:
	ipAddress = ""
	pageUrl = ""

	def __init__(self, ipAddress, domain, pageUrl="", dateTime="", userAgent=""):
		self.ipAddress = ipAddress
		self.domain = domain
		self.pageUrl = pageUrl
		self.dateTime = dateTime
		self.userAgent = userAgent

	def __str__(self):
		return "{} - {} {} - {} - {} ".format(self.ipAddress, self.domain, self.pageUrl, self.dateTime, self.userAgent[:30])
		