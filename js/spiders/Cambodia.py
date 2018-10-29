# -*- coding: utf-8 -*-
import datetime
import hashlib
import re

import scrapy
from scrapy import Request

from js.items import JsItem


class CambodiaSpider(scrapy.Spider):
    name = 'Cambodia'
    allowed_domains = ['jcairlines.com']
    urls = 'https://www.jcairlines.com/#/bookTicket/choose/searchType=1&goDate={time}&startCity={start}&endCity={end}&tab=1?_k=4y6esb'

    luxian = {'XIY': ['KOS', 'REP'], 'TPE': ['PNH'], 'XUZ': ['REP'], 'CKG': ['KOS', 'PNH', 'REP'],
              'SIN':['PNH'],'CAN':["KOS"],'HKG': ['KOS', 'PNH', 'REP'] ,'KMG':['REP'],'XIY':['KOS','REP'],
              'XUZ':['REP'],'KWE':['REP'],'HIA':['REP'],'SYX':['PNH'],'HFE':['PNH']
              }
    # luxian = {'XIY': ['KOS', 'REP']}

    def start_requests(self):
        for key in self.luxian.keys():
            for value in self.luxian.get(key):
                # 爬取30天的航班信息
                for day in range(0,30):
                    time=self.get_timedata(day)
                    url=self.urls.format(time=time,start=key,end=value)
                    # print(url)
                    yield Request(url=url,dont_filter=True,callback=self.parse,meta={'key':'ppppppp'})
        # yield Request(url="https://www.jcairlines.com/#/bookTicket/choose/searchType=1&goDate=2018-10-26&startCity=CKG&endCity=REP&tab=1?_k=4y6esb",dont_filter=True,callback=self.parse)
    # 新加坡H'}
    # def start_requests(self):
    #     yield r\
    def parse(self, response):
        Item=JsItem()

        if self.isElementExist(response,'//*[contains(@class,"airline-cell-30")]/span//text()'):

                Item['if_data']=True
                Item["id_url"] = self.get_md5(response.url)
                Item["name"] = self.remove_kongge(
                    response.xpath('//*[contains(@class,"choose-ticket-company")]/span/text()').extract())
                Item["url"] = response.url
                Item["startname"] = response.xpath('//*[contains(@class,"airline-cell-30")]/span//text()')[0].extract()
                Item["endname"] = response.xpath('//*[contains(@class,"airline-cell-30")]/span//text()')[1].extract()
                Item["starttime"] = response.xpath('//*[contains(@class,"airline-cell-40" )]/span//text()')[0].extract()
                Item["endtime"] = response.xpath('//*[contains(@class,"airline-cell-40" )]/span//text()')[2].extract()
                Item["mun"] = response.xpath('//*[contains(@class,"airline-cell-40" )]/span//text()')[1].extract()
                ss = self.get_mun(self.remove_kongge(
                    response.xpath('//*[contains(@class,"choose-ticket-price-info-other")]/span[2]//text()').extract()))
                try:
                    price_list = []
                    y = 0
                    for i in response.xpath('//*[contains(@class,"priceNew" )]/text()').extract():
                        ifpublic = response.xpath('//*[contains(@class,"price-name-new")]//text()')[y].extract()
                        pricell = str(int(i) + ss) + "$ " + ifpublic
                        y += 1
                        price_list.append(pricell)
                    Item["price_list"]=price_list
                except:

                    Item['if_data'] = False
        return Item


    def get_md5(self,url):
        md5 = hashlib.md5()
        md5.update(url.encode(encoding='utf-8'))
        return md5.hexdigest()

    def remove_kongge(self,titles):
        ss = "".join(titles)
        ss = ss.replace(' ', '').replace('\n', ' ')
        return ss

    def get_mun(self,ss):
        re_compile = re.compile("\d+")
        findall = re.findall(re_compile, ss)
        return int(findall[0])

    def isElementExist(self, response,ss):
        try:
            print(response)
            response.xpath(ss)[0]
            print(True)
            return True
        except:
            print(False)
            return False
    def get_timedata(self,i):
        ISOTIMEFORMAT = '%Y-%m-%d'
        theTime = datetime.datetime.now()
        Time = (theTime + datetime.timedelta(days=i)).strftime(ISOTIMEFORMAT)
        return str(Time)