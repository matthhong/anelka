from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as LinkExtract
from scrapy.selector import Selector
from anelka_scrape.items import Transfer

class PlayersSpider(CrawlSpider):
    name = "anelka"
    allowed_domains = ["transfermarkt.co.uk"]
    start_urls = ["http://www.transfermarkt.co.uk/en/nicolas-anelka/transfers/spieler_3226.html"]
    
    rules = (Rule(LinkExtract(allow = ['transfers\/verein', '\/kader\/', 'profil'], deny = 'historische-kader')),
             Rule(LinkExtract(allow = 'transfers\/spieler', restrict_xpaths = '//div[@id="left"]'), 
                  callback = 'person_parse'))

    def person_parse(self, response):
        sel = Selector(response)
        tData = sel.xpath('//p[text()="Transfer history"]/following::table[@class="tabelle_grafik"]//td//text()').extract()[8:-3]
        tData = [tData[i:i+13] for i in range(0, len(tData), 13)] #partition into different transfers
        
        person = sel.xpath('//title/text()').extract()[0][:-57]
        transfers = []
        for t in tData:
            transfer = Transfer()
            transfer['person'] = person
            transfer['date'] = t[1].split('.')[::-1] #make compatible with datetime.datetime(y,m,d)
            transfer['fro'] = t[4]
            transfer['to'] = t[7]
            transfers.append(transfer)
        return transfers
            
        