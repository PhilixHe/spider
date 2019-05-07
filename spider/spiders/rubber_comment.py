# -*- coding: utf-8 -*-
import scrapy
import logging
from ..items import db_session, RubberJP


class RubberCommentSpider(scrapy.Spider):
    name = 'rubber_comment'
    allowed_domains = ['takkyu-navi.jp']

    def start_requests(self):
        url = 'https://takkyu-navi.jp/rubber/detail/'
        rubbers = db_session.query(RubberJP).all()
        for rubber in rubbers:
            yield scrapy.Request(url='%s%s' % (url, rubber.rubberid), meta={'rubber_id': rubber.rubberid},
                                 callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            rubber_id = response.meta['rubber_id']
            comments_page_urls = response.xpath('//div[@id="usrRevBlk"]/ol[@class="pager"]//li[not('
                                                '@class="disabled")]/a/@href').getall()
            for url in list(set(comments_page_urls)):
                yield response.follow(url, callback=self.comment_page_parse, meta={'rubber_id': rubber_id})

        else:
            logging.error("+++++++++++++++++++Request URL: %s \tHTTP Code: %s" % (response.url, response.status))

    def comment_page_parse(self, response):
        if response.status == 200:
            rubber_id = response.meta['rubber_id']
            comments = self.comments_parse(response)

            yield {'rubber_id': rubber_id, 'comments': comments}

        else:
            logging.error("+++++++++++++++++++Request URL: %s \tHTTP Code: %s" % (response.url, response.status))

    def comments_parse(self, response):
        comments = response.xpath('//div[@id="usrRevBlk"]/ul//li')
        comment_set = []
        for comment in comments:

            name_node = comment.xpath('.//dt[@class="usrBox clearfix"]//em[@itemprop="author"]')
            name = name_node.xpath('string(.)').get().strip()

            trs = comment.xpath('.//dd[@class="usrEvl clearfix"]//div[@class="floatR"]/table//tr')
            attribute = []
            for tr in trs:
                attribute.append(tr.xpath('string(.)').get().split())

            description = comment.xpath('.//dd[@class="usrEvl clearfix"]//div[@class="comnt"]['
                                        '@itemprop="description"]/p').xpath('string(.)').get()
            date = comment.xpath('.//dd[@class="usrEvl clearfix"]//small[@class="date"]/text()').get()
            cm = dict()
            cm['name'] = name
            cm['attribute'] = attribute
            cm['description'] = description
            cm['date'] = date
            comment_set.append(cm)

        return comment_set
