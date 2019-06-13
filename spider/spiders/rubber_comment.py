# -*- coding: utf-8 -*-
import scrapy
import logging
from ..items import db_session, RubberJP
from ..spiders import table_tennis_comments_parse


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
            comments = table_tennis_comments_parse(response)

            yield {'rubber_id': rubber_id, 'comments': comments}

        else:
            logging.error("+++++++++++++++++++Request URL: %s \tHTTP Code: %s" % (response.url, response.status))
