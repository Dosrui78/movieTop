# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from maoyan.items import MaoyanItem
from scrapy.selector import Selector

class MovietopSpider(Spider):
    name = 'movie'
    allowed_domains = ['maoyan.com']
    start_urls = 'https://maoyan.com/board/4?offset='

    def start_requests(self):
        for i in range(10):
            url = self.start_urls + str(i * 10)
            yield Request(url=url,callback=self.parse, dont_filter=True)

    def parse(self, response):
        sel = Selector(response)
        items = sel.xpath('//dl[@class="board-wrapper"]/dd')
        for c in items:
            item = MaoyanItem()
            item['rank'] = ''.join(c.xpath('./i/text()').extract()).strip()
            item['title'] = ''.join(c.xpath('.//p[@class="name"]/a/text()').extract()).strip()
            item['actor'] = ''.join(c.xpath('.//p[@class="star"]/text()').extract()).strip()
            item['time'] = ''.join(c.xpath('.//p[@class="releasetime"]/text()').extract()).strip()
            item['score'] = ''.join(c.xpath('.//p[@class="score"]//text()').extract()).strip()
            yield item
