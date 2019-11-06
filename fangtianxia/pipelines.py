# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter


class FangtianxiaPipeline(object):
    def __init__(self):
        self.newhouse_fp_csv = open('newhouse.csv', 'wb')
        self.newhouse_exporter_csv = CsvItemExporter(self.newhouse_fp_csv)

    def process_item(self, item, spider):
        self.newhouse_exporter_csv.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_fp_csv.close()
