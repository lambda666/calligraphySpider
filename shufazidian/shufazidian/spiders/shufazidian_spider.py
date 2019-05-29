import scrapy
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from shufazidian.items import ShufazidianItem

style_dict = {
    '行书':'8',
    '楷书':'9',
    '草书':'7',
    '隶书':'6',
    '魏碑':'5',
    '简牍':'4',
    '篆书':'3',
    '设计师专用':'shiliang',
    '钢笔':'gangbi',
    '篆刻':'zhuangke'
}

class ShufazidianSpider(scrapy.Spider):
    name = 'shufazidian'
    allowed_domains = ['shufazidian.com', 'blog.csdn.net']

    start_urls = ['https://blog.csdn.net/deathkon/article/details/78216492']

    shufazidian_url = 'http://www.shufazidian.com/'

    def parse(self, response):
        '''从CSDN博客文章中获取常用汉字'''
        
        page = Selector(response)

        # 获取博客网页中的汉字，做成列表
        content = page.xpath("//div[@id='content_views']/p/text()").extract()[0].split(' ')[0:-1]
        
        # 发送一个请求到书法字典网主页，并把汉字列表传递给后续的函数来处理
        yield Request(self.shufazidian_url, callback = self.parse_shufazidian, meta={'content':content})


    def parse_shufazidian(self, response):
        '''提交汉字到书法字典网，获取汉字的书法字帖'''

        # 取出汉字列表并遍历
        content = response.meta['content']
        for key,value in style_dict.items():
            for c in content:
                # 提交post请求，获取字帖
                # 表格参数中wd是查询的汉字，sort是书法字体
                yield FormRequest.from_response(
                    response,
                    method='POST',
                    formxpath='//form[@name="form1"]',
                    formdata={'wd':c, 'sort':value},
                    callback=self.parse_page,
                    meta={'style':key}
                )

    def parse_page(self, response):
        '''解析网页中字帖图片的url'''
        style = response.meta['style']
        page = Selector(response)
        # 字帖列表有固定结构，按照这个结构来提取字帖图片
        for sel in page.xpath("/html/body/div[3]/div[2]/div[1]/div[2]/div"):
            item = ShufazidianItem()
            # 字帖标题
            item['title'] = sel.xpath('div/div//text()').extract()[0]
            # 字帖图片地址
            item['image_urls'] = [sel.xpath('div/div/a/img/@src').extract()[0]]
            # 当前查询的汉字
            item['category'] = sel.xpath('//form[@name="form1"]/input[@id="wd"]/@value').extract()[0]
            # 当前字体
            item['style'] = style
            yield item
