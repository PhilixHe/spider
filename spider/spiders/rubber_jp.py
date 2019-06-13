# -*- coding: utf-8 -*-
import scrapy
import logging
from ..items import db_session, RubberJP
from ..spiders import table_tennis_comments_parse


class RubberJPSpider(scrapy.Spider):
    name = 'rubber_jp'
    allowed_domains = ['takkyu-navi.jp']

    def start_requests(self):
        switch = True
        rubberid = 1
        url = 'https://takkyu-navi.jp/rubber/detail/'

        while switch:
            racket = db_session.query(db_session.query(RubberJP).filter(RubberJP.rubberid == rubberid).exists()).scalar()
            if not racket:
                yield scrapy.Request(url='%s%s' % (url, rubberid), callback=self.parse)
                rubberid += 1

    def parse(self, response):
        if response.status == 200:
            items = dict()
            items['rubberid'] = response.url.split('/')[-1]

            items['name'] = response.xpath('//*[@id="dtlMainBlk"]/h2/text()').get()

            td2 = response.xpath('//*[@id="dtlMainBlk"]/div/div[@class="top-hardness MB10"][1]/table//td['
                                 '@class="top-content"]')
            rate = td2.xpath('string(.)').get()
            if rate:
                rate = rate.strip()

            items['rate'] = rate

            items['price'] = response.xpath('//*[@id="dtlMainBlk"]/div/div[@class="top-hardness MB10"][2]//span['
                                            '@class="top-numerical"]/text()').get()

            items['img_link'] = response.xpath('//*[@id="dtlMainBlk"]/div/div[@class="imgBox clearfix"]/div['
                                               '@class="floatL"]//img/@src').get()

            items['property'] = response.xpath(
                '//*[@id="dtlMainBlk"]//div[@class="pointBoxWrap"]//span/text()').extract()

            desc_dom = response.xpath('//*[@id="dtlMainBlk"]/div//dl[@class="desc"]')
            items['description'] = desc_dom.xpath('string(.)').get()

            items['classify'] = response.xpath('//*[@id="dtlMainBlk"]/div/ul//span/text()').extract()

            specifications = []
            for div in response.xpath('//*[@id="dtlMainBlk"]//div[@class="dataBox2"]//div'):
                for i in div.xpath('*'):
                    key = i.xpath('*')[0].xpath('string(.)').get().strip()
                    val = i.xpath('*')[1].xpath('string(.)').get().strip()
                    specifications.append([key, val])
            items['specifications'] = specifications

            first_page_comments = table_tennis_comments_parse(response)
            items['comments'] = first_page_comments
            yield items

        else:
            logging.error("+++++++++++++++++++Request URL: %s \tHTTP Code: %s" % (response.url, response.status))
