# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import db_session, Racket, Rubber, RacketJP, RubberJP
import logging
import json


class SpiderPipeline(object):
    def process_item(self, item, spider):
        spider_name = spider.name
        if spider_name == 'racket':
            raclet = Racket(
                racketid=item['racketid'],
                name=item['name'],
                rate=item['rate'],
                img_link=item['img_link'],
                property=json.dumps(item['property']),
                classify=json.dumps(item['classify']),
                description=item['description'],
                specifications=json.dumps(item['specifications'])
            )
            db_session.add(raclet)
            db_session.commit()

        elif spider_name == 'rubber':
            rubber = Rubber(
                rubberid=item['rubberid'],
                name=item['name'],
                rate=item['rate'],
                img_link=item['img_link'],
                property=json.dumps(item['property']),
                classify=json.dumps(item['classify']),
                description=item['description'],
                specifications=json.dumps(item['specifications'])
            )
            db_session.add(rubber)
            db_session.commit()

        elif spider_name == 'racket_jp':
            raclet = RacketJP(
                racketid=item['racketid'],
                name=item['name'],
                rate=item['rate'],
                price=item['price'],
                img_link=item['img_link'],
                property=json.dumps(item['property']),
                classify=json.dumps(item['classify']),
                description=item['description'],
                specifications=json.dumps(item['specifications'])
            )
            db_session.add(raclet)
            db_session.commit()

        elif spider_name == 'rubber_jp':
            rubber = RubberJP(
                rubberid=item['rubberid'],
                name=item['name'],
                rate=item['rate'],
                price=item['price'],
                img_link=item['img_link'],
                property=json.dumps(item['property']),
                classify=json.dumps(item['classify']),
                description=item['description'],
                specifications=json.dumps(item['specifications'])
            )
            db_session.add(rubber)
            db_session.commit()

        else:

            return None

        return item
