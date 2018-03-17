# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

	
class tbcommentItem(Item):
    content = Field()  # 评论的内容
    creation_time = Field()  # 评论创建的时间
    product_url = Field()  # 商品的链接
    product_sku = Field()  # 商品的分类
    product_title = Field()  # 商品的描述
    product_id = Field()  # 商品的id
    product_price = Field()  # 商品的价格
    user_nickname = Field()  # 评论用户的名字
    user_viplevel = Field()  # 评论用户的vip等级
    user_rank = Field()   # 评论用户的购买数量
    user_anony = Field()   # 评论用户是否匿名
    save_time = Field()   # 抓取数据的时间
    user_id = Field()   # 店铺ID
