from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


entry_tag = Table('entry_tags', Base.metadata,
                  Column('entry_id', Integer, ForeignKey('entry.id')),
                  Column('tag_id', Integer, ForeignKey('tag.id')))


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    stop = Column(DateTime)
    note = Column(String)
    tags = relationship('Tag', secondary=entry_tag, back_populates='entries')

    @property
    def duration(self):
        pass


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    entries = relationship('Entry', secondary=entry_tag, back_populates='tags')

