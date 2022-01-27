import logging
import os
import pymongo
from scrapy.exceptions import DropItem


class RozetkaPipeline(object):
    def __init__(self):
        db_name = os.getenv('DB_NAME') if os.getenv('DB_NAME') else "rozetka"
        db_user = os.getenv('DB_USERNAME')
        db_pass = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        #client = pymongo.MongoClient("mongodb://localhost:27017/rozetka")
        client = pymongo.MongoClient(f"mongodb://{db_host}")
        self.db = client[db_name]
        self.collection = self.db['product']

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))
        #logging.info(str(item))
        index = self.db.product.insert(dict(item))
        return f"index: {index}"
