# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time
import json
import xlwt
import pymysql

class StatePipeline(object):
    def open_spider(self,spider):
        self.jsonfile=open("jiuchang.json","w",encoding="utf-8")
        self.jsonfile.write("["+"\n")
        self.first=1
    def process_item(self, item, spider):
        if self.first == 1:
            movie=json.dumps(dict(item),ensure_ascii=False)
            self.jsonfile.write(movie)
            self.first=0
        else:
            movie=",\n"+json.dumps(dict(item),ensure_ascii=False)
            self.jsonfile.write(movie)
        return  item
    def close_spider(self,spider):
        self.jsonfile.write("\n"+"]")
        self.jsonfile.close()

# 存入数据库

class MysqlPipeline(object):
    def open_spider(self,spider):
        args={
            'host':'localhost',
            'port':3306,
            'user':'root',
            'password':'123456',
            'db':'scrapy_winery',
            'charset':'utf8'
        }
        try:
            self.connection=pymysql.connect(**args)
            self.cur=self.connection.cursor()
        except Exception as e:
            print("数据库连接失败或游标创建失败")
    def process_item(self,item,spider):
        
        sql='insert into state_winery_into values (%s,%s,%s,%s,%s,%s)'
        print("item:", item)
        param = (item['winery_name'], item['address'], item['phone'], item['time'],item['locations'],item['type'])
        rowscount=self.cur.execute(sql, param)
        if rowscount:
            print("写入数据成功")
        self.connection.commit()
        print("事务提交成功")

        return item


    def close_spider(self,spider):
        # self.connection.commit()
        print("事务提交成功")
        self.cur.close()
        print("游标关闭成功")
        self.connection.close()
# class StatePipeline(object):
#     def process_item(self, item, spider):
#         return item
