# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    wuyeleibie = scrapy.Field()
    xiangmutese = scrapy.Field()
    jianzhuleibie = scrapy.Field()
    zhuangxiuzhuangkuang = scrapy.Field()
    chanquannianxian = scrapy.Field()
    huanxianweizhi = scrapy.Field()
    kaifashang = scrapy.Field()
    loupandizhi = scrapy.Field()
    xiaoshouzhuangtai = scrapy.Field()
    loupanyouhui = scrapy.Field()
    kaipanshijian = scrapy.Field()
    jiaofangshijian = scrapy.Field()
    shouloudizhi = scrapy.Field()
    ziundianhua = scrapy.Field()
    zhulihuxing = scrapy.Field()
    yushouxuke = scrapy.Field()
    url = scrapy.Field()


class ESFHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    unit = scrapy.Field()
    origin_url = scrapy.Field()