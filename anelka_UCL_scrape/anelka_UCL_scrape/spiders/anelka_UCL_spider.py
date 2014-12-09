from scrapy.spider import Spider
from anelka_UCL_scrape.items import Passes

end = 2011883
start = 2011739

class PassesSpider(Spider):
	name = "passes"
	allowed_domains = [ "http://www.uefa.com/" ]
	start_urls = [ "http://www.uefa.com/" ]

	def parse(self, response):
		yield Passes(
			file_urls = [ 
				self.start_urls[0] + "newsfiles/ucl/2014/" + str(i) + "_tl.pdf" \
				for i in range(start, end + 1)])
