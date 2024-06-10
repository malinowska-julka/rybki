# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter

class RybkiScrapyCSVExporter():

    '''def open_spider(self):
        #vrkvr
    def close_spider(self, spider):

        #    exporter.finish_exporting()
         #   rybki_csv.close()
'''
    def exporter_for_item(self, item):
        rybki_csv = open('~/Desktop/rybki/rybki.csv', 'w')
        exporter = CsvItemExporter(file=rybki_csv, include_headers_line=True)
        exporter.start_exporting()

    def process_item(self, item, spider):
        exporter = self.exporter_for_item(item)
        exporter.export_item(item)
        return item