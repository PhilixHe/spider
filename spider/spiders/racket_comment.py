# -*- coding: utf-8 -*-
import scrapy
import logging
from ..items import db_session, RacketJP


class RubberCommentSpider(scrapy.Spider):
    name = 'racket_comment'
    allowed_domains = ['takkyu-navi.jp']

    def start_requests(self):
        url = 'https://takkyu-navi.jp/racket/detail/'
        rackets = db_session.query(RacketJP).all()
        for racket in rackets:
            yield scrapy.Request(url='%s%s' % (url, racket.racketid), meta={'racket_id': racket.racketid},
                                 callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            racket_id = response.meta['racket_id']
            comments_page_urls = response.xpath('//div[@id="usrRevBlk"]/ol[@class="pager"]//li[not('
                                                '@class="disabled")]/a/@href').getall()
            for url in list(set(comments_page_urls)):
                yield response.follow(url, callback=self.comment_page_parse, meta={'racket_id': racket_id})

        else:
            logging.error("+++++++++++++++++++Request URL: %s \tHTTP Code: %s" % (response.url, response.status))

    def comment_page_parse(self, response):
        if response.status == 200:
            racket_id = response.meta['racket_id']
            comments = self.comments_parse(response)

            yield {'racket_id': racket_id, 'comments': comments}

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
