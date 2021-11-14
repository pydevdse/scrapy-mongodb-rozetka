# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class RozetkaItem(Item):
    #id = Field()
    sku = Field()
    url = Field()
    name = Field()
    image = Field()
    description = Field()
    price = Field()
    priceCurrency = Field()
    priceValidUntil = Field()
    brand = Field()
