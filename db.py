from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, Text
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Posts(Base):
    __tablename__ = 'posts'

    # id = Column(Integer, primary_key=True)
    message = Column(UnicodeText)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    post_id = Column(Text, primary_key=True)
    image_url = Column(Text)

    def __repr__(self):
        return "<Post(message='%s', id='%s')>" % (
            self.message, self.post_id)


class JodelDB():
    def __init__(self):
        self.engine = create_engine('sqlite:///foo.db', echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)
