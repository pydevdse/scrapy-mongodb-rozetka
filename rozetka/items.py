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
    characteristics = Field()
