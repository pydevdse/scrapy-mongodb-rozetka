import logging
import json
import scrapy
from ..items import RozetkaItem

logging.basicConfig(level=logging.INFO)

class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    start_urls = ['https://hard.rozetka.com.ua/hdd/c80084/']
    COUNT_PAGES = 2
    #url = 'https://hard.rozetka.com.ua/hdd/c80084/'
    """
    def start_requests(self):
        response = scrapy.Request(self.url)
        #pages = response.xpath('//li[@class="pagination__item ng-star-inserted"]/text()')
        #print(pages[len(pages)-1].get())
        print(dir(response))
        return
    """

    def parse(self, response):
        pages = response.xpath('//a[@class="pagination__link ng-star-inserted"]//text()')
        pages = int(pages[-1].get()) if len(pages)>3 else None
        if not pages:
            return
        logging.info(f'PAGES: {pages}')
        for page in range(1, pages+1)[:2]:
            url = self.start_urls[0] + f'page={page}/'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for title in response.xpath('.//a[@class="goods-tile__heading ng-star-inserted"]'):
            url = title.xpath('.//@href').extract_first()
            #logging.info(url)
            yield scrapy.Request(url, callback=self.parse_product)


    def parse_product(self, response):
        product_json = json.loads(response.xpath('.//script[@data-seo="Product"]/text()').extract_first())
        meta = response.meta
        meta['product'] = product_json
        yield scrapy.Request(response.url+'characteristics/', meta=meta, callback=self.parse_characteristics)

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
