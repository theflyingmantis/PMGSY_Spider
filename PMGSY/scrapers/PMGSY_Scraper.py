import scrapy

class PMGSYScraper:
	"""

	"""
	def getDistrictName(self,rowResponse):
		columns = rowResponse.css('td div::text').extract()
		return columns[1].strip().encode('utf-8')

	def getDistrictData(self,rowResponse):
		columns = rowResponse.css('td')
		data = []
		for i in range(2,44):
			data.append(columns[i].css('div::text').extract_first())
		return data

	def getDataInAnchorTag(self,selector):
		return selector.css('a::text').extract_first().strip().replace('\n', ' ').replace('\r', '').encode('utf-8')

