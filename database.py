from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import tweepy
import datetime
import os
from dotenv import load_dotenv


load_dotenv()
API_Key     = os.getenv("API_KEY")
API_Sec     = os.getenv("API_SEC")
Token       = os.getenv("TOKEN")
Token_Sec   = os.getenv("TOKEN_SEC")


# engine = create_engine('sqlite:///test.db')
# DB_URI = os.getenv("DB_URI")
# engine = create_engine(DB_URI)
engine = create_engine(os.getenv('DATABASE_URL').replace('postgres', 'postgresql'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
import models


def init_db():
    Base.metadata.create_all(bind=engine)


def get_trends():
    datum = db_session.query(models.Ttrends).order_by(models.Ttrends.created.desc()).limit(24)
    
    trends = []
    for data in datum:
        date = str(data.created.month)+'月'+str(data.created.day)+'日'+str(data.created.hour)+'時'
        topics = []
        for i, t in enumerate(data.trends):
            topics.append({'rank': i+1, 'topic': t[0], 'url': t[1]})
        
        trend = {'date': date, 'topics': topics}
        trends.append(trend)

    return trends


def store_ttrends():
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(API_Key, API_Sec)
    auth.set_access_token(Token, Token_Sec)
    api = tweepy.API(auth)

    #日本のWOEID
    woeid = 23424856
    #トレンド一覧取得
    ttrends = api.get_place_trends(woeid)
    l = ttrends[0]['trends']
    trends = []
    for d in l:
        trends.append(list(d.values()))

    # 現在の日本の時刻
    now = datetime.datetime.now()

    t = models.Ttrends(trends=trends, created=now)
    db_session.add(t)
    db_session.commit()

    return


def delete_ttrends():
    now = datetime.datetime.now()
    last = now + datetime.timedelta(days=-31)

    data = db_session.query(models.Ttrends).filter(models.Ttrends.created < now).all()
    db_session.delete(data)
    db_session.commit()

    return
