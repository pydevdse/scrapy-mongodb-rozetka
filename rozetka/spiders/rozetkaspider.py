import json
import scrapy
from ..items import RozetkaItem

class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    start_urls = ['https://hard.rozetka.com.ua/hdd/c80084/']
    COUNT_PAGES = 1
    
    def parse(self, response):
        for title in response.xpath('.//a[@class="goods-tile__heading ng-star-inserted"]'):
            yield response.follow(url=title.xpath('.//@href').extract_first(), callback=self.parse_product)
        if self.COUNT_PAGES > 0:
            self.COUNT_PAGES -= 1
            next_page = response.xpath('//a[@class="button button_color_gray button_size_medium pagination__direction pagination__direction_type_forward ng-star-inserted"]/@href').extract_first()
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        product_json = json.loads(response.xpath('.//script[@data-seo="Product"]/text()').extract_first())
        meta = response.meta
        meta['product'] = product_json
        yield response.follow(response.url+'characteristics/', meta=meta, callback=self.parse_characteristics)

    def parse_characteristics(self, response):
        product_json = response.meta['product']
        characteristics = []
        for c in response.xpath('//section/dl[@class="characteristics-full__list"]/div[@class="characteristics-full__item ng-star-inserted"]'):
            parametr_label = c.xpath('.//dt[@class="characteristics-full__label"]/span//text()').extract_first()
            parametr_value = c.xpath('.//dd[@class="characteristics-full__value"]/ul/li//text()').extract_first()
            characteristics.append({'label': parametr_label, 'value': parametr_value})

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
        item['characteristics'] = characteristics
        yield item
