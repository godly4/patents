# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class PatentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()
    applyNum = Field()
    publicNum = Field()
    classifyNum = Field()
    mainClassifyNum = Field()
    name = Field()
    publicDate = Field()
    applyDate = Field()
    agentPer = Field()
    agent = Field()
    agentDis = Field()
    agentType = Field()
    newestLaw = Field()
    ambit = Field()
    abstract = Field()
    claim = Field()
    code = Field()
    applyPer = Field()
    investPer = Field()
    prior = Field()
    pageNum = Field()
    address = Field()
    oldLaw = Field()
    ajax = Field()
    typeT = Field()
    other = Field()
    agentCode = Field()
