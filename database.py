from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///test.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
import models


def init_db():
    Base.metadata.create_all(bind=engine)


def get_trends():
    datum = db_session.query(models.Trends).order_by(models.Trends.created.desc()).limit(12)
    
    trends = []
    for data in datum:
        date = str(data.created.month)+'月'+str(data.created.day)+'日'+str(data.created.hour)+'時'
        topics = []
        for i, t in enumerate(data.trends):
            topics.append({'rank': i+1, 'topic': t[0], 'url': t[1]})
        
        trend = {'date': date, 'topics': topics}
        trends.append(trend)

    return trends