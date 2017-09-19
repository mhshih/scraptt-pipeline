# -*- coding: utf-8 -*-
"""Database handlers."""
from sqlalchemy import (
    create_engine, Column, ForeignKey,
    String, TEXT, Integer, DateTime
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URI = 'postgresql+psycopg2://postgres:1234@scraptt-db:54321'
DB_NAME = 'scraptt'

engine = create_engine(f'{URI}/{DB_NAME}', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Post(Base):
    """PTT POST table."""

    __tablename__ = 'post'

    id = Column(String, primary_key=True)
    board = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    published = Column(DateTime, nullable=False, index=True)
    crawled = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, index=True)
    content = Column(TEXT, nullable=False)


class Comment(Base):
    """PTT COMMENT table."""

    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published = Column(DateTime, nullable=False, index=True)
    crawled = Column(DateTime, nullable=False)
    content = Column(TEXT, nullable=False)
    post_id = Column(String, ForeignKey('post.id'), nullable=True, index=True)


class Meta(Base):
    """PTT Meta table."""

    __tablename__ = 'meta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    translate = Column(String, nullable=True, unique=True)


def init_db():
    """Initialize database."""
    _engine = create_engine(URI)
    session = sessionmaker(bind=_engine)()
    session.connection().connection.set_isolation_level(0)
    # create database
    session.execute(f'CREATE DATABASE {DB_NAME}')
    session.close()
    # create tables
    Base.metadata.create_all(engine)
