# -*- coding: utf-8 -*-
"""Database handlers."""
import os

from sqlalchemy import (
    create_engine, Column, ForeignKey, TypeDecorator,
    String, TEXT, CHAR, Integer, DateTime
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ProgrammingError

URI = (
    'cockroachdb://{COCKROACHDB_USER}@{COCKROACHDB_HOST}:{COCKROACHDB_PORT}/'
    .format(**os.environ)
)
PARAMS = '?sslmode=disable'
DB_NAME = 'scraptt'

engine = create_engine(f'{URI}{DB_NAME}{PARAMS}', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class CommentType(TypeDecorator):
    """Custom type for comment type."""

    impl = Integer

    mappings = {
        '噓': -1,
        '→': 0,
        '推': 1,
    }

    mappings_r = {v: k for k, v in mappings.items()}

    def process_literal_param(self, value, dialect):
        """Convert text to int."""
        return self.mappings[value]
    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect):
        """Convert sql int to meaningful text."""
        return self.mappings_r[value]


class Comment(Base):
    """PTT COMMENT table."""

    __tablename__ = 'comment'

    id = Column(CHAR(16), primary_key=True)
    type = Column(CommentType, nullable=False)
    author = Column(String, nullable=False)
    published = Column(DateTime, nullable=False, index=True)
    crawled = Column(DateTime, nullable=False)
    content = Column(TEXT, nullable=False)
    ip = Column(String, nullable=True)
    post_id = Column(String, ForeignKey('post.id'), nullable=True, index=True)


class Post(Base):
    """PTT POST table."""

    __tablename__ = 'post'

    id = Column(String, primary_key=True)
    board = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    published = Column(DateTime, nullable=False, index=True)
    crawled = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    content = Column(TEXT, nullable=False)
    ip = Column(String, nullable=True)
    upvote = Column(Integer)  # 推文數量
    novote = Column(Integer)  # → 數量
    downvote = Column(Integer)  # 噓文數量
    comments = relationship(Comment, backref='post')

    @property
    def url(self):
        """Return URL."""
        return f'https://www.ptt.cc/bbs/{self.board}/{self.id}.html'


class Meta(Base):
    """PTT Meta table."""

    __tablename__ = 'meta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    translate = Column(String, nullable=True, unique=True)


def init_db():
    """Initialize database."""
    _engine = create_engine(f'{URI}system{PARAMS}')
    session = sessionmaker(bind=_engine)()
    session.connection().connection.set_isolation_level(0)
    # create database
    try:
        session.execute(f'CREATE DATABASE {DB_NAME}')
        session.close()
        # create tables
        Base.metadata.create_all(engine)
    except ProgrammingError as e:
        if 'already exists' in e.args[0]:
            pass
        else:
            raise(e)
