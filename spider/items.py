# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, Text, Table
from sqlalchemy.orm import relationship, backref
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


class Rubber(Base):
    __tablename__ = "Rubber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rubberid = Column(Integer, default=0, index=True)
    name = Column(String(255), default='')
    rate = Column(String(255), default='')
    img_link = Column(String(255), default='')
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


class Sportsman(Base):
    __tablename__ = "Sportsman"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, default=0, index=True)
    name = Column(String(100), default='')
    img_link = Column(String(255), default='')
    description = Column(Text, default='')
    info = Column(Text, default='[]')


sportsman_racket_rubber = Table('sportsman_racket_rubber',
                                Base.metadata,
                                Column('id', Integer, primary_key=True, autoincrement=True),
                                Column('sportsman_id', Integer, ForeignKey("Sportsman.id")),
                                Column('racket_id', Integer, ForeignKey("RacketJP.id")),
                                Column('rubber_id', Integer, ForeignKey("RubberJP.id")))


class RubberJP(Base):
    __tablename__ = "RubberJP"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rubberid = Column(Integer, default=0, index=True)
    name = Column(String(255), default='')
    rate = Column(String(255), default='')
    price = Column(String(100), default='0')
    img_link = Column(String(255), default='')
    property = Column(Text, default='[]')
    classify = Column(Text, default='[]')
    description = Column(Text, default='')
    # json数据 eg: [["Producer", 'Butterfly'], ["Product code", "23950"]]
    specifications = Column(Text, default='[]')
    sportsmans = relationship("Sportsman", backref="rubber_jp", secondary=sportsman_racket_rubber)


class RacketJP(Base):
    __tablename__ = "RacketJP"

    id = Column(Integer, primary_key=True, autoincrement=True)
    racketid = Column(Integer, default=0, index=True)
    name = Column(String(255), default='')
    rate = Column(String(255), default='')
    price = Column(String(100), default='0')
    img_link = Column(String(255), default='')
    property = Column(Text, default='[]')
    classify = Column(Text, default='[]')
    description = Column(Text, default='')
    # json 数据 eg: [["Speed", "12.4"], ["Touch", "12.5"]]
    specifications = Column(Text, default='[]')
    sportsmans = relationship("Sportsman", backref="racket_jp", secondary=sportsman_racket_rubber)


class Comments(Base):
    __tablename__ = "Comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    racket_id = Column(Integer, ForeignKey('RacketJP.id', ondelete="CASCADE"), nullable=True, default=None)
    rubber_id = Column(Integer, ForeignKey('RubberJP.id', ondelete="CASCADE"), nullable=True, default=None)
    racket = relationship('RacketJP', backref=backref('comments'))
    rubber = relationship('RubberJP', backref=backref('comments'))
    name = Column(String(255), default='')
    attribute = Column(Text, default='[]')
    description = Column(Text, default='')
    date = Column(String(50), default='')


Base.metadata.create_all(engine)
