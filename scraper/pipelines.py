from scraper.models import *
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker


class DbPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_newsdata_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        newsdata = NewsData(**item)

        exist_file_id = session.query(NewsData).filter_by(file_id=item["file_id"]).first()
        if exist_file_id is not None:  # the current article exists
            raise DropItem(f"Duplicate item found: {item['file_id']}")
            session.close()
        else:
            try:
                session.add(newsdata)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return item