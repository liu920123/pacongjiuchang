# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field() #国家名
    urlone=scrapy.Field() #国家的超链接

    winery=scrapy.Field() #酒厂名
    urlthree=scrapy.Field() #跟进的链接
    type=scrapy.Field() #酒厂类型


    winery_name=scrapy.Field() #酿酒公司
    address=scrapy.Field() #公司的地址
    phone=scrapy.Field() #电话
    time=scrapy.Field() #营业时间
    locations=scrapy.Field() #相关地点
    
    
    
    last_updated = scrapy.Field(serializer=str)
    pass
