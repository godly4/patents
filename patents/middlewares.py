# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from useragents import agents

class PatentUaMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(agents)
        request.headers["User-Agent"] = ua
