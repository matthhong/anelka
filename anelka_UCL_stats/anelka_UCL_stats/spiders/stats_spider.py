from scrapy.selector import Selector
from scrapy.spider import Spider
from anelka_UCL_stats.items import Stats

class StatsSpider(Spider):
	name = "stats"
	allowed_domains = [ "www.uefa.com" ]
	start_urls = [ 'http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000478/match=' + str(i) + '/postmatch/statistics' for i in range(2011739,2011759)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000479/match=' + str(i) + '/postmatch/statistics' for i in range(2011759,2011855)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000480/match=' + str(i) + '/postmatch/statistics' for i in range(2011855,2011871)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000481/match=' + str(i) + '/postmatch/statistics' for i in range(2011871,2011879)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000482/match=' + str(i) + '/postmatch/statistics' for i in range(2011879,2011883)] + \
		['http://www.uefa.com/uefachampionsleague/season=2014/matches/round=2000483/match=2011883/postmatch/statistics']

	def parse(self, response):
		sel = Selector(response)
		stats = Stats()
		stats['game'] = response.url[80:87]
		stats['playerStats'] = sel.xpath("//tbody//text()").extract()[-432:]
		return stats

# Team stats: Goals, Possession, Total Att, On Target, Off Target, blocked, Woodwork, Corners, Offsides, YC, RC, Fouls committed,
# Fouls suffered, Passes, Completed Passes.

# Player stats: Goals, On target, off target, Assists, Offsides, Fouls Committed, Fouls Suffered, Passes, Completed passes.