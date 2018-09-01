"""Elasticsearch pipeline."""
import os

from jseg import Jieba
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import (
    Document,
    Text,
    Integer,
    Date,
)

j = Jieba()
connections.create_connection(
    hosts=['{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'.format(**os.environ)],
)


def seg_str(text):
    """Segmentate strings."""
    if not text:
        return ''
    output = ' '.join(j.seg(text))
    return output


class Doc(Document):
    """Elasticsearch document."""

    post_type = Integer(required=True)
    board = Text(required=True)
    author = Text(required=True)
    published = Date(required=True)
    title = Text()
    content = Text(required=True)
    ip = Text()
    upvote = Integer()
    novote = Integer()
    downvote = Integer()
    type = Text()
    post_id = Text()

    class Index:
        """Index info."""

        name = 'ptt'


class AlchemyDoc(Doc):
    """ES Doc for SQLAlcheymy."""

    def __init__(self, *args, **kwargs):
        """Post process for fields."""
        kwargs.pop('_sa_instance_state')
        kwargs.pop('crawled')
        if 'title' in kwargs:
            kwargs['title'] = seg_str(kwargs['title'])
        kwargs['content'] = seg_str(kwargs['content'])
        if 'comments' in kwargs:
            kwargs['post_type'] = 0
            kwargs.pop('comments')
        else:
            kwargs['post_type'] = 1
        super().__init__(*args, **kwargs)
        self.meta.id = kwargs.pop('id')


class CockroachDoc(Doc):
    """ES Doc for CockroachDB."""

    def __init__(self, *args, **kwargs):
        """Post process for fields."""
        if 'title' in kwargs:
            kwargs['title'] = seg_str(kwargs['title'])
        kwargs['content'] = seg_str(kwargs['content'])
        super().__init__(*args, **kwargs)
        self.meta.id = kwargs.pop('id')
