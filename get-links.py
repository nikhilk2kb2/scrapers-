import scrapy 


class IecSpider(scrapy.Spider):
	name = 'iec'

	start_urls = ('http://www.iec-iab.be/nl/diensten/zoeken/Pages/Zoeken.aspx?all=true&org=on',)

	def parse(self, response):
		txt = '\n'.join(response.urljoin(i) for i in response.css('ul.searchresults li>a::attr(href)').extract())
		with open('iec-links.txt', 'ab') as f:
			f.write(txt)

		nxt = response.css('a.next::attr(href)').extract_first()
		if nxt:
			yield scrapy.Request(response.urljoin(nxt), callback=self.parse)
