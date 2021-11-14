# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import json
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem


class RozetkaPipeline(object):
    def __init__(self): # mongodb://YourUsername:YourPasswordHere@127.0.0.1:27017/your-database-name

        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USERNAME')
        db_pass = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        client = pymongo.MongoClient(f"mongodb://{db_host}:{db_port}/{db_name}")
        self.db = client[db_name]
        self.collection = self.db['product']

    def process_item(self, item, spider):

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        index = self.db.product.insert(dict(item))
        return f"index: {index}"

