"""Dump data from CockroachDB to Elasticsearch."""
from cockroach.db import Session, Post
from cockroach.es import Doc

s = Session()

for doc in s.query(Post):
    Doc(**doc.__dict__).save()
    for comment in doc.comments:
        comment.board = doc.board
        Doc(**comment.__dict__).save()
