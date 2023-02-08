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


# engine = create_engine("sqlite:///test.db")
engine = create_engine(os.getenv("DATABASE_URL").replace("postgres", "postgresql"))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
import models


# テーブルの作成
def init_db():
    Base.metadata.create_all(bind=engine)


# 表示させるTwitterのトレンドの取得
def get_trends():
    # 24時間のデータ取得
    datum = db_session.query(models.Ttrends).order_by(models.Ttrends.created.desc()).limit(24)
    
    trends = []
    for data in datum:
        date = str(data.created.month)+"月"+str(data.created.day)+"日"+str(data.created.hour)+"時"
        topics = []
        for i, t in enumerate(data.trends):
            topics.append({"rank": i+1, "topic": t[0], "url": t[1]})
        
        trend = {"date": date, "topics": topics}
        trends.append(trend)

    return trends


# dateのTwitterのトレンドを取得
def search_trends(date):
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    td_1d = datetime.timedelta(days=1)
    datum = db_session.query(models.Ttrends).filter(d <= models.Ttrends.created, models.Ttrends.created < d + td_1d)

    trends = []
    for data in datum:
        date = str(data.created.month)+"月"+str(data.created.day)+"日"+str(data.created.hour)+"時"
        topics = []
        for i, t in enumerate(data.trends):
            topics.append({"rank": i+1, "topic": t[0], "url": t[1]})
        
        trend = {"date": date, "topics": topics}
        trends.append(trend)

    return trends


# 現在のTwitterトレンドを保存
def store_ttrends():
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(API_Key, API_Sec)
    auth.set_access_token(Token, Token_Sec)
    api = tweepy.API(auth)

    # 日本のWOEID
    woeid = 23424856
    # トレンド一覧取得
    ttrends = api.get_place_trends(woeid)
    l = ttrends[0]["trends"]
    trends = []
    for d in l:
        trends.append(list(d.values()))

    # 現在の時刻
    now = datetime.datetime.now()

    t = models.Ttrends(trends=trends, created=now)
    db_session.add(t)
    db_session.commit()

    print("stored twitter trends.")

    return


# Twitterのトレンドのデータを削除
# 動いていない
def delete_ttrends():
    # 31日以上前のデータを対象
    now = datetime.datetime.now()
    last = now + datetime.timedelta(days=-31)

    data = db_session.query(models.Ttrends).filter(models.Ttrends.created < last).all()
    db_session.delete(data)
    db_session.commit()

    print("deleted twitter trends.(" + str(len(data)) + ")")

    return
