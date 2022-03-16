from sqlalchemy import Column, Integer, DateTime, PickleType
from database import Base


class Ttrends(Base):
    __tablename__ = 'twitter_trends'
    id = Column(Integer, primary_key=True)
    trends = Column(PickleType)
    created = Column(DateTime)


    def __init__(self, trends=None, created=None):
        self.trends = trends
        self.created = created


    def __repr__(self):
        return f'id={self.id!r}\ntrends={self.trends}\ncreatedat={self.created}'
    