"""Dump data from CockroachDB to Elasticsearch."""
from cockroach.db import Session, Post
from cockroach.es import AlchemyDoc

s = Session()

for doc in s.query(Post):
    AlchemyDoc(**doc.__dict__).save()
    for comment in doc.comments:
        comment.board = doc.board
        AlchemyDoc(**comment.__dict__).save()
