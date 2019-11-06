# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter, CsvItemExporter


class FangtianxiaPipeline(object):
    def __init__(self):
        self.newhouse_fp = open('newhouse.json', 'wb')
        self.newhouse_fp_csv = open('newhouse.csv', 'wb')
        self.newhouse_exporter_json = JsonLinesItemExporter(self.newhouse_fp, ensure_ascii=False)
        self.newhouse_exporter_csv = CsvItemExporter(self.newhouse_fp_csv)

    def process_item(self, item, spider):
        self.newhouse_exporter_json.export_item(item)
        self.newhouse_exporter_csv.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_fp.close()
