import tweepy
import datetime
import os
from dotenv import load_dotenv
from database import db_session
from models import Trends


load_dotenv()
API_Key     = os.getenv("API_KEY")
API_Sec     = os.getenv("API_SEC")
Token       = os.getenv("TOKEN")
Token_Sec   = os.getenv("TOKEN_SEC")


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
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=tz_jst)

    t = Trends(trends=trends, created=now)
    db_session.add(t)
    db_session.commit()

    return