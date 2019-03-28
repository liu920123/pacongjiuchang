# -*- coding: utf-8 -*-
import scrapy
from ..items import StateItem

class StatespiderSpider(scrapy.Spider):
    name = 'Statespider'
    allowed_domains = ['ratebeer.com']
    start_urls = 'https://www.ratebeer.com/breweries/'

    def start_requests(self):
        yield scrapy.Request(self.start_urls,callback=self.parse)

    def parse(self, response):
        """

        :param response:
        :return:
        """
        items=[]
        for li in response.xpath('//*[@id="default"]/a'):
            item = StateItem()
            name=li.xpath('text()').extract() #国家名
            urlone=li.xpath('@href').extract() #需要跟进的链接


            item['name']=''.join(name)
            item['urlone']="https://www.ratebeer.com/breweries"+''.join(urlone)

            print(item['urlone'])
            # yield item
            items.append(item)

        headers = {'referer': response.url}
        for item in items:
            yield scrapy.Request(item['urlone'],callback=self.two_parse,dont_filter=True,meta={"item": item},headers=headers)
            # print("url地址:"+item['urlone'])

    def two_parse(self,response):
        """
        链接跟进
        :param response:
        :return:
        """



        type_list = []
        for li in response.xpath("//div[contains(@id,'active') or contains(@id,'closed')]/table//tr"):
            # item = StateItem()
            type=li.xpath('td[2]//text()').extract() or [""]
            print("type:", type)
            # item['type']=type[0]
            type_list.append(type[0])

        for index, li in enumerate(response.xpath('//*/div/div/div/div/div/div/table//tr//a[1]')):
            # item = StateItem()
            winery = li.xpath('text()').extract() #酒厂名
            print(winery)
            urlthree = li.xpath('@href').extract() #需要跟进的链接
            # item['winery']=winery[0] #酒厂名
            url="https://www.ratebeer.com"+''.join(urlthree)
            # yield item
            yield scrapy.Request(url,callback=self.detail_parse,dont_filter=True,meta={"type":type_list[index]})

    def detail_parse(self,response):
        item = StateItem()
        winery_name=response.xpath('//*/div/h1/text()').extract() #酿酒公司
        address=response.xpath('//*/div/span/span/a//text()').extract() #地址
        phone=response.xpath('//*/div/span/a/text()').extract() #电话
        time=response.xpath('//*/div[@class="container-fluid"]/div/div/span/div[2]/text()').extract() #营业时间
        locations=response.xpath('//*/div[@class="container-fluid"]/div/div/div/b//text()').extract() #相关地点


        item['winery_name']=winery_name[0]

        try:
            item['address']=''.join(address)
        except:
            item['address']=None
        try:
            item['phone']=phone[0]
        except:
            item['phone']=None
        try:
            item['time']=''.join(time)
        except:
            item['time']=None
        try:
            item['locations']=''.join(locations)
        except:
            item['locations']=None
        item["type"] = response.meta["type"]
        print("item:", item)
        yield item



        pass
