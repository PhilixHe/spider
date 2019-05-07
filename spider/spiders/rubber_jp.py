# -*- coding: utf-8 -*-
import scrapy
import logging
from ..items import db_session, RubberJP


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

            items['description'] = response.xpath(
                '//*[@id="dtlMainBlk"]/div/dl/dd[@itemprop="description"]//p/text()').get()

            items['classify'] = response.xpath('//*[@id="dtlMainBlk"]/div/ul//span/text()').extract()

            specifications = []
            for div in response.xpath('//*[@id="dtlMainBlk"]//div[@class="dataBox2"]//div'):
                for i in div.xpath('*'):
                    key = i.xpath('*')[0].xpath('string(.)').get().strip()
                    val = i.xpath('*')[1].xpath('string(.)').get().strip()
                    specifications.append([key, val])
            items['specifications'] = specifications

            first_page_comments = self.comments_parse(response)
            items['comments'] = first_page_comments
            yield items

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
