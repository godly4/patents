# -*- coding: utf-8 -*-
import re
import json
import uuid
import scrapy
import requests
import redis
import logging
from scrapy.http import Request
from patents.items import PatentsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging
from scrapy.linkextractors import LinkExtractor

configure_logging(install_root_handler=False)
#定义了logging的些属性
logging.basicConfig(
    filename='scrapy.log',
    format='%(levelname)s: %(levelname)s: %(message)s',
    level=logging.INFO
)
#运行时追加模式
logger = logging.getLogger('SimilarFace')

def getArray(array, index):
    ret = ""
    if len(array) > index:
        ret = array[index]

    return ret

def getAjax(url):
    ret = ""
    try:
        r = requests.get(url)
        ret = ','.join(json.loads(r.text))
    except:
        pass
    
    return ret

class ColpatentsSpider(CrawlSpider):
    name = "colpatents"
    region = {
        'A': '人类生活必需',
        'B': '作业;运输',
        'C': '化学;冶金',
        'D': '纺织;造纸',
        'E': '固定建筑物',
        'F': '机械工程;照明;加热;武器;爆破;',
        'G': '物理',
        'H': '电学',
    }

    def start_requests(self):
        for page in range(1, 39590):
            url = "http://patentool.wanfangdata.com.cn/Patent/Search?Query=%E5%9C%B0%E5%9D%80%3A%E5%B9%BF%E4%B8%9C%E7%9C%81&Page={0}&Count=50&SortBy=sortby%20relevance&DisplayWay=list".format(page)
            yield Request(url=url, callback=self.parseList)

    def parseList(self, response):
        links = response.xpath("//span[contains(@class,'sePatentname')]/a/@href").extract()
        for link in links:
            url = "http://patentool.wanfangdata.com.cn/{0}".format(link)
            yield Request(url=url, callback=self.parsePatent)

    def parsePatent(self, response):
        tdList = response.xpath('//tr/td').extract()
        applyNum = getArray(re.findall("<span.*>(.*)</span",tdList[21]),0)
        publicNum = getArray(re.findall("<span.*>(.*)</span",tdList[26]),0)
        classifyNum = getArray(re.findall("<span.*>(.*)</span",tdList[34]),0)
        mainClassifyNum = getArray(re.findall("<span.*>(.*)</span",tdList[30]),0)
        name = getArray(re.findall("<td.*>(.*)</td",tdList[1]),0)
        publicDate = getArray(re.findall("<span.*>(.*)</span",tdList[16]),0)
        applyDate = getArray(re.findall("<span.*>(.*)</span",tdList[11]),0)
        agentPer = getArray(re.findall("<span.*>(.*)</span",tdList[28]),0)
        agent = getArray(re.findall("<td.*>(.*)</td",tdList[23]),0)
        agentDis = ""
        agentType = ""
        lawStatus = response.xpath('//span[@class="CDPLawStatus"]/text()').extract()
        newestLaw = lawStatus[1]
        oldLaw = " ".join(lawStatus)
        ambit = ""
        if mainClassifyNum and mainClassifyNum[0] in self.region:
            ambit = self.region[mainClassifyNum[0]]
        abstract = getArray(re.findall("<span.*>(.*)</span",tdList[7]),0)
        claim = getArray(re.findall("<span.*>(.*)</span",tdList[9]),0)
        code = getArray(re.findall("<span.*>(.*)</span",tdList[36]),0)
        applyPer = getArray(re.findall("<span.*>(.*)</span",tdList[13]),0)
        investPer = getArray(re.findall("<span.*>(.*)</span",tdList[18]),0)
        prior = ""
        pageNum = ""
        address = getArray(re.findall("<span.*>(.*)</span",tdList[32]),0)
        ajax = getAjax("http://patentool.wanfangdata.com.cn/Patent/AutoTag?articleId={0}".format(applyNum))
        typeT = getArray(re.findall("<td.*>(.*)</td",tdList[3]),0)
        other = ""
        agentCode = ""

        patentItem = PatentsItem()
        patentItem["_id"] = str(uuid.uuid1())
        patentItem["applyNum"] = applyNum
        patentItem["publicNum"] = publicNum
        patentItem["classifyNum"] = classifyNum
        patentItem["mainClassifyNum"] = mainClassifyNum
        patentItem["name"] = name
        patentItem["publicDate"] = publicDate
        patentItem["applyDate"] = applyDate
        patentItem["agentPer"] = agentPer
        patentItem["agent"] = agent
        patentItem["agentDis"] = agentDis
        patentItem["agentType"] = agentType
        patentItem["newestLaw"] = newestLaw
        patentItem["ambit"] = ambit
        patentItem["abstract"] = abstract
        patentItem["claim"] = claim
        patentItem["code"] = code
        patentItem["applyPer"] = applyPer
        patentItem["investPer"] = investPer
        patentItem["prior"] = prior
        patentItem["pageNum"] = pageNum
        patentItem["address"] = address
        patentItem["oldLaw"] = oldLaw
        patentItem["ajax"] = ajax
        patentItem["typeT"] = typeT
        patentItem["other"] = other
        patentItem["agentCode"] = agentCode

        yield patentItem
