# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import log

SETTINGS = get_project_settings()

class CommentPipeline(object):
    def process_item(self, item, spider):
        return item

		
class TBCommentPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        # Instantiate DB
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host=SETTINGS['DB_HOST'],
                                            user=SETTINGS['DB_USER'],
                                            passwd=SETTINGS['DB_PASSWD'],
                                            port=SETTINGS['DB_PORT'],
                                            db=SETTINGS['DB_DB'],
                                            charset='utf8',
                                            use_unicode=True,
                                            cursorclass=MySQLdb.cursors.DictCursor
                                            )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):
        content = item['content']
        creation_time = item['creation_time']
        product_url = item['product_url']
        product_sku = item['product_sku']
        product_title = item['product_title']
        product_id = item['product_id']
        product_price = item['product_price']
        user_nickname = item['user_nickname']
        user_viplevel = item['user_viplevel']
        user_rank = item['user_rank']
        user_anony = item['user_anony']
        save_time = item['save_time']
        user_id = item['user_id']

        sql = "INSERT INTO item_%s VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (user_id, content, creation_time, product_url, product_sku, product_title, product_id, \
               product_price, user_nickname, user_viplevel, user_rank, user_anony, save_time)

        tx.execute(sql)
        print "yes"

    def _handle_error(self, e):
        log.err(e)
