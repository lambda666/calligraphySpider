# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShufazidianItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()

    # 分类的标题
    category = scrapy.Field()
    # 图片地址
    image_urls = scrapy.Field()

    images = scrapy.Field()