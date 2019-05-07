# -*- coding: utf-8 -*-
import scrapy
import logging
from ..items import db_session, RacketJP, RubberJP, Sportsman


class SportsmanSpider(scrapy.Spider):
    name = 'sportsman'
    allowed_domains = ['takkyu-navi.jp']

    def start_requests(self):
        switch = True
        player_id = 1
        url = 'https://takkyu-navi.jp/player/detail/'

        while switch:
            sportsman = db_session.query(db_session.query(Sportsman).filter(Sportsman.player_id == player_id).exists()).scalar()
            if not sportsman:
                yield scrapy.Request(url='%s%s' % (url, player_id), meta={'player_id': player_id}, callback=self.parse)
            player_id += 1

    def parse(self, response):
        if response.status == 200:
            name = response.xpath('//*[@id="dtlMainBlk"]/h2/text()').get()
            if name is not None:
                items = dict()
                items['name'] = name.strip()
                items['player_id'] = response.meta['player_id']

                items['img_link'] = response.xpath('//*[@id="dtlMainBlk"]/div[@class="inner"]//div[@class="col-sm-5 '
                                                   'modalThums"]//a[@href="#myModal_1"][1]/img/@src').get()

                items['description'] = response.xpath('//*[@id="dtlMainBlk"]/div[@class="inner"]//dd['
                                                      '@itemprop="description"]//p/text()').get()

                info = []
                for div in response.xpath('//*[@id="dtlMainBlk"]//div[@class="dataBox2"]//div'):
                    for i in div.xpath('*'):
                        key = i.xpath('*')[0].xpath('string(.)').get().strip()
                        val = i.xpath('*')[1].xpath('string(.)').get().strip()
                        info.append([key, val])
                items['info'] = info
                rele_data = []
                racket_and_rubber = response.xpath('//*[@id="dtlMainBlk"]/div[@class="inner"]//div[@class="col-sm-7 '
                                                   'usingRub"]/ol//li')
                for i in racket_and_rubber:
                    url = i.xpath('./a/@href').get()
                    level = url.split('/')
                    rid = level[-1]
                    res = level[-3]
                    rele_data.append([res, rid])
                items['rele_data'] = rele_data
                return items

            logging.error("+++++++++++++++++++Request URL: %s \tPage is None!!!" % response.url)
        else:
            logging.error("+++++++++++++++++++Request URL: %s \tHTTP Code: %s" % (response.url, response.status))
