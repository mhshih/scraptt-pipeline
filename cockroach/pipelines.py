# -*- coding: utf-8 -*-
"""Scrapy pipeilnes."""
from hashlib import sha256
import logging

from .db import Session, Post, Comment, Meta

logger = logging.getLogger(__name__)


class BasePipeline:
    """Handle session while open/close spider."""

    def open_spider(self, spider):
        """Build database connection."""
        self.session = Session()
        logger.debug('DB connected.')

    def close_spider(self, spider):
        """Close database connectoin."""
        self.session.close()
        logger.debug('DB disconnected.')


class PTTPipeline(BasePipeline):
    """Insert PTT POST and COMMENT into database."""

    def process_item(self, item, spider):
        """Insert data into database."""
        post_obj = Post(
            id=item['id'],
            board=item['board'],
            author=item['author'],
            published=item['time']['published'],
            crawled=item['time']['crawled'],
            title=item['title'],
            ip=item['ip'],
            content=item['content'],
            upvote=item['count']['推'],
            novote=item['count']['→'],
            downvote=item['count']['噓'],
        )
        self.session.merge(post_obj)
        for comment in item['comments']:
            hashid = sha256((
                f"{item['id']}"
                f"{comment['author']}"
                f"{comment['time']['published']}"
            ).encode('utf-8')).hexdigest()[:16]
            comment_obj = Comment(
                id=hashid,
                type=comment['type'],
                author=comment['author'],
                published=comment['time']['published'],
                crawled=comment['time']['crawled'],
                ip=comment['ip'],
                content=comment['content'],
                post_id=item['id'],
            )
            self.session.merge(comment_obj)
        self.session.commit()
        return item


class MetaPipeline(BasePipeline):
    """Insert PTT meta-data into database."""

    def process_item(self, item, spider):
        """Insert data into database."""
        meta_obj = Meta(
            name=item['name']
        )
        self.session.merge(meta_obj)
        self.session.commit()
        return item
