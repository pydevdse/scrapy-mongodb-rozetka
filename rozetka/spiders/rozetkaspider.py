import os
import json
import scrapy
from ..items import RozetkaItem

class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    start_urls = ['https://hard.rozetka.com.ua/hdd/c80084/']
    COUNT_PAGES = 1
    
    def parse(self, response):
        for title in response.xpath('.//a[@class="goods-tile__heading ng-star-inserted"]'):

            post = {
                'title': title.xpath('.//text()').get(),
                'url': title.xpath('.//@href').extract_first(),
                #'price': title.xpath('.//p[@class="ng-star-inserted"]/span[@class="goods-tile__price-value"]/text()')
                    #.get().replace('\xa0', '').strip()
            }
            meta = response.meta
            meta['post'] = post
            yield response.follow(url=title.xpath('.//@href').extract_first(), callback=self.parse_product, meta=meta)
        if self.COUNT_PAGES > 0:
            self.COUNT_PAGES -= 1
            next_page = response.xpath('//a[@class="button button_color_gray button_size_medium pagination__direction pagination__direction_type_forward ng-star-inserted"]/@href').extract_first()
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        product_json = json.loads(response.xpath('.//script[@data-seo="Product"]/text()').extract_first())
        item = RozetkaItem()
        #item['id']
        item['sku'] = product_json['sku']
        item['url'] = product_json['url']
        item['name'] = product_json['name']
        item['image'] = product_json['image']
        item['description'] = product_json['description']
        item['price'] = product_json['offers']['price']
        item['priceCurrency'] = product_json['offers']['priceCurrency']
        item['priceValidUntil'] = product_json['offers']['priceValidUntil']
        item['brand'] = product_json['brand']['name']
        yield item
