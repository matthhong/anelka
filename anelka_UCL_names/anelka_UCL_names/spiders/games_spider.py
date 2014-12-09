from scrapy.selector import Selector
from scrapy.spider import Spider
from anelka_UCL_names.items import Teams

class NamesSpider(Spider):
	name = "names"
	allowed_domains = [ "www.uefa.com" ]
	start_urls = [ 'http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000478/match=' + str(i) for i in range(2011739,2011759)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000479/match=' + str(i) for i in range(2011759,2011855)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000480/match=' + str(i) for i in range(2011855,2011871)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000481/match=' + str(i) for i in range(2011871,2011874)]

	def parse(self, response):
		sel = Selector(response)
		names = sel.xpath('//div[@class="mb-team-name"]/a/text()').extract()
		teams = Teams()
		teams['home'] = names[0]
		teams['away'] = names[1]
		teams['gid'] = response.url[-8:-1]
		return teams