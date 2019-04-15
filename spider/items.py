# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, Text
from sqlalchemy.orm import sessionmaker, scoped_session

from .config import DATABASE

engine = create_engine('mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
    database=DATABASE['database'],
    username=DATABASE['username'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']), echo=False)

Session = scoped_session(sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False,
))

db_session = Session()
Base = declarative_base()


# class RubberItem(scrapy.Item):
#     rubber_id = scrapy.Field()
#     name = scrapy.Field()
#     img_link = scrapy.Field()
#     rate = scrapy.Field()
#     property = scrapy.Field()
#     specifications = scrapy.Field()

# class RacketItem(scrapy.Item):
#     racket_id = scrapy.Field()
#     name = scrapy.Field()
#     img_link = scrapy.Field()
#     rate = scrapy.Field()
#     property = scrapy.Field()
#     specifications = scrapy.Field()


class Rubber(Base):
    __tablename__ = "Rubber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rubberid = Column(Integer, default=0, index=True)
    name = Column(String(255), default='')
    img_link = Column(String(255), default='')
    rate = Column(String(255), default='')
    property = Column(Text, default='[]')
    classify = Column(Text, default='[]')
    description = Column(Text, default='')
    # json数据 eg: [["Producer", 'Butterfly'], ["Product code", "23950"]]
    specifications = Column(Text, default='[]')


class Racket(Base):
    __tablename__ = "Racket"

    id = Column(Integer, primary_key=True, autoincrement=True)
    racketid = Column(Integer, default=0, index=True)
    name = Column(String(255), default='')
    rate = Column(String(255), default='')
    img_link = Column(String(255), default='')
    property = Column(Text, default='[]')
    classify = Column(Text, default='[]')
    description = Column(Text, default='')
    # json 数据 eg: [["Speed", "12.4"], ["Touch", "12.5"]]
    specifications = Column(Text, default='[]')


Base.metadata.create_all(engine)
