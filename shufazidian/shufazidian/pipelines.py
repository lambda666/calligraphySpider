# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
import re

class ShufazidianPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 下载图片
        #print('get_media_request')
        #print(item['image_urls'])
        #print(item['title'])
        yield scrapy.Request(url=item['image_urls'][0], meta={'title':item['title'], 'category':item['category']})
    
    def item_completed(self, results, item, info):
        #print('item_completed')
        # 是否下载成功
        if not results[0]:
            raise scrapy.DropItem('download error')
        return item

    def file_path(self, request, response=None, info=None):
        # 生成下载图片的文件名
        #print('file_path')
        title = request.meta['title']
        category = request.meta['category']
        image_name = request.url.split('/')[-1]
        folder_strip = re.sub(r'[?\\*|"<>:/]', '', str(title))
        filename = u'{0}/{1}/{2}'.format(category, folder_strip, image_name)
        #print(filename)
        return filename

