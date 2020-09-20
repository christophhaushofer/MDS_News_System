import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from scraper.settings import *
from sqlalchemy.orm import sessionmaker

DeclarativeBase = declarative_base()


def db_connect():
    db_url = URL(**DATABASE)
    logging.info("Creating an SQLAlchemy engine at URL '{db_url}'".format(db_url=db_url))
    return create_engine(db_url)


def create_newsdata_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class NewsData(DeclarativeBase):
    __tablename__ = "news_data"

    id = Column(Integer, primary_key=True)
    file_id = Column('file_id', String)
    headline = Column('headline', String)
    title = Column('title', String)
    link = Column('link', String)
    description = Column('description', String)
    content = Column('content', String)
    author = Column('author', String)
    pubDate = Column('pubDate', DateTime(timezone=True))
    source = Column('source', String)
'''
class ClusterData(DeclarativeBase):
    __tablename__ = "cluster_data_test"

    id = Column(Integer, primary_key=True)
    cluster = Column('cluster', Integer)
    sim_article_id = Column('sim_article_id', String)
    author = Column('author', String)
    pubDate = Column('pubDate', DateTime(timezone=True))
    source = Column('source', String)

def TestDB(data):

    engine = db_connect()
    create_newsdata_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    clusters = ClusterData(**data)
    try:
        session.add(clusters)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
'''