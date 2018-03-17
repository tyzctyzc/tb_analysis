#-*- coding: utf-8 -*-

import sys
import chardet
import re
import json
import datetime
import config
import utils
import time
import logging
import random
import xlwt
import xlrd

from scrapy.http.cookies import CookieJar
from scrapy.utils.project import get_project_settings
from scrapy import Spider
from scrapy import Request
from tb.items import tbcommentItem

reload(sys)
sys.setdefaultencoding('utf-8')


class TBSpider(Spider):
    name = 'tb_comment'

    def __init__(self, name = None, **kwargs):
        super(TBSpider, self).__init__(name, **kwargs)
        self.url = kwargs.get("url")
        self.guid = kwargs.get('guid', 'guid')
        pattern = re.compile('user-rate-')
        urls = re.split(pattern, self.url)
        user_id = urls[1]
        pattern = re.compile('\w+', re.S)
        self.user_id = re.search(pattern, user_id).group()
        self.log('user_id:%s' % self.user_id)
        self.item_table = 'item_%s' % self.user_id

        self.log_dir = 'log'
        self.is_record_page = False
        self.sql = kwargs.get('sql')
        self.red = kwargs.get('red')
        item_table = self.item_table
        workbook=xlwt.Workbook(encoding='utf-8')  
        booksheet=workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)  
        data=(('user_id','guid'),  
              (self.user_id,self.guid),  
              )  
        for i,row in enumerate(data):  
            for j,col in enumerate(row):  
                booksheet.write(i,j,col)  
        workbook.save('user_id.xls') 		
        self.init()

    def init(self):
        command = (
            "CREATE TABLE IF NOT EXISTS `{}` ("
            "`content` TEXT NOT NULL,"  # 评论的内容
            "`creation_time` CHAR(200) DEFAULT NULL,"  # 评论创建的时间
            "`product_url` CHAR(200) DEFAULT NULL,"  # 商品的链接
            "`product_sku` CHAR(50) DEFAULT NULL,"  # 商品的分类
            "`product_title` CHAR(50) DEFAULT NULL,"  # 商品的描述
            "`product_id` CHAR(20) DEFAULT NULL,"  # 商品的id
            "`product_price` CHAR(10) DEFAULT NULL,"  # 商品的价格
            "`user_nickname` CHAR(20) DEFAULT NULL,"  # 评论用户的名字
            "`user_viplevel` INT(5) DEFAULT NULL,"  # 评论用户的vip等级
            "`user_rank` INT(10) DEFAULT NULL,"  # 评论用户的购买数量
            "`user_anony` CHAR(10) DEFAULT NULL,"  # 评论用户是否匿名
            "`save_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"  # 抓取数据的时间
            ") ENGINE=InnoDB".format(self.item_table))
        logging.warn(command)
        self.sql.create_table(command)

#        utils.push_redis(self.guid, self.user_id, '开始抓取淘宝店铺该商品的评价信息...')

    xlrd.Book.encoding = "utf-8"
    data = xlrd.open_workbook("user_id.xls")
    table = data.sheets()[0]
    user_ids = table.col_values(0)  # 商品ID
    guids = table.col_values(1)  # 商品评论数
    user_id = user_ids[1]
    guid = guids[1]
    page = 2
    start_urls = []
    for i in range(1, page):  # 一件商品一件商品的抽取
        pagestr = ""
        if i > 0:
            pagestr = "&page=%d" % i
        url = "https://rate.taobao.com/member_rate.htm?_ksTS=" + guid + "&callback=shop_rate_list&content=1&result=&from=rate&" \
               + "user_id=" + user_id + "&identity=1&rater=0&direction=0" + pagestr
        logging.warn(url)
        start_urls.append(url)

    def parse(self, response):
        temp1 = response.body.split('watershed')
        str = '{"watershed' + temp1[1][:-7]
        str = str.decode("gbk").encode("utf-8")
        js = json.loads(unicode(str, "utf-8"))
        comments = js['rateListDetail']  # 该页所有评论
        items = []
        for comment in comments:
            logging.warning("comment")
            logging.warning(comment)
            item1 = tbcommentItem()
            item1['content'] = comment.get('content')  # 评论的内容
            item1['creation_time'] = comment.get('date', '')  # 评论创建的时间
            item1['product_url'] = comment['auction']['link']  # 商品的链接
            item1['product_sku'] = comment['auction']['sku']  # 商品的分类
            item1['product_title'] = comment['auction']['title']  # 商品的描述
            item1['product_id'] = comment['auction']['aucNumId']  # 商品的id
            item1['product_price'] = comment['auction']['auctionPrice']  # 商品的价格
            item1['user_nickname'] = comment['user']['nick']  # 评论用户的名字
            item1['user_viplevel'] = comment['user']['vipLevel']  # 评论用户的vip等级
            item1['user_rank'] = comment['user']['rank']  # 评论用户的购买数量
            item1['user_anony'] = comment['user']['anony']  # 评论用户是否匿名
            item1['save_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 抓取数据的时间
            item1['user_id'] = self.user_id  # 店铺id
            items.append(item1)
        return items
