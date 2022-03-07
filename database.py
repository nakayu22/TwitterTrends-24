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
    data = db_session.query(models.Trends).first()
    
    date = str(data.created.month)+'月'+str(data.created.day)+'日'+str(data.created.hour)+'時'
    topics = []
    for t in data.trends:
        topics.append({'topic': t[0], 'url': t[1]})
    
    trend = {'date': date, 'topics': topics}

    return trend