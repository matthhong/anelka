from scrapy.item import Item, Field

class Transfer(Item):
    person = Field()
    date = Field()
    fro = Field()
    to = Field()