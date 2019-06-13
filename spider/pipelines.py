# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import db_session, Racket, Rubber, RacketJP, RubberJP, Comments, Sportsman
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
            racket = RacketJP(
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

            for com in item['comments']:
                racket.comments.append(Comments(
                    name=com['name'],
                    chart_head=com['chart_head'],
                    table_tennis_history=com['table_tennis_history'],
                    attribute=json.dumps(com['attribute']),
                    description=com['description'],
                    recommend=json.dumps(com['recommend']),
                    date=com['date'],
                    praise=com['praise']
                ))
            db_session.add(racket)
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

            for com in item['comments']:
                rubber.comments.append(Comments(
                    name=com['name'],
                    chart_head=com['chart_head'],
                    table_tennis_history=com['table_tennis_history'],
                    attribute=json.dumps(com['attribute']),
                    description=com['description'],
                    recommend=json.dumps(com['recommend']),
                    date=com['date'],
                    praise=com['praise']
                ))

            db_session.add(rubber)
            db_session.commit()

        elif spider_name == 'rubber_comment':
            rubber_id = item['rubber_id']
            rubber_jp = db_session.query(RubberJP).filter(RubberJP.rubberid == rubber_id).one()
            comments = []
            for comment in item['comments']:
                rubber_comment = Comments(
                    rubber=rubber_jp,
                    name=comment['name'],
                    chart_head=comment['chart_head'],
                    table_tennis_history=comment['table_tennis_history'],
                    attribute=json.dumps(comment['attribute']),
                    description=comment['description'],
                    recommend=json.dumps(comment['recommend']),
                    date=comment['date'],
                    praise=comment['praise']
                )
                comments.append(rubber_comment)

            db_session.add_all(comments)
            db_session.commit()

        elif spider_name == 'racket_comment':
            racket_id = item['racket_id']
            racket_jp = db_session.query(RacketJP).filter(RacketJP.racketid == racket_id).one()
            comments = []
            for comment in item['comments']:
                rubber_comment = Comments(
                    racket=racket_jp,
                    name=comment['name'],
                    chart_head=comment['chart_head'],
                    table_tennis_history=comment['table_tennis_history'],
                    attribute=json.dumps(comment['attribute']),
                    description=comment['description'],
                    recommend=json.dumps(comment['recommend']),
                    date=comment['date'],
                    praise=comment['praise']
                )
                comments.append(rubber_comment)

            db_session.add_all(comments)
            db_session.commit()

        elif spider_name == 'sportsman':

            sportsman = Sportsman(
                player_id=item['player_id'],
                name=item['name'],
                img_link=item['img_link'],
                description=item['description'],
                info=json.dumps(item['info'])
            )
            for ite in item['rele_data']:
                if ite[0] == 'racket':
                    racket_jp = db_session.query(RacketJP).filter(RacketJP.racketid == ite[1]).scalar()
                    if racket_jp:
                        sportsman.racket_jp.append(racket_jp)

                elif ite[0] == 'rubber':
                    rubber_jp = db_session.query(RubberJP).filter(RubberJP.rubberid == ite[1]).scalar()
                    if rubber_jp:
                        sportsman.rubber_jp.append(rubber_jp)

            db_session.add(sportsman)
            db_session.commit()

        else:

            return None

        return '===============<Store successful>==============='
