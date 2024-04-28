from sqlalchemy import Column, Integer, String, Date
from database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    content = Column(String(250))
    date_posted = Column(Date)

    def __init__(self, title=None, content=None, date_posted=None):
        self.title = title
        self.content = content
        self.date_posted = date_posted
