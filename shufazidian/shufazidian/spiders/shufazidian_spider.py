import scrapy
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from shufazidian.items import ShufazidianItem

class ShufazidianSpider(scrapy.Spider):
    name = 'shufazidian'
    allowed_domains = ['shufazidian.com', 'blog.csdn.net']

    start_urls = ['https://blog.csdn.net/deathkon/article/details/78216492']

    shufazidian_url = 'http://www.shufazidian.com/'

    def parse(self, response):
        page = Selector(response)
        content = page.xpath("//div[@id='content_views']/p/text()").extract()[0].split(' ')[0:-1]
        #print(content)
        yield Request(self.shufazidian_url, callback = self.parse_hanzi, meta={'content':content})


    def parse_hanzi(self, response):
        content = response.meta['content']
        #print(content)
        for c in content:
            yield FormRequest.from_response(
                response,
                method='POST',
                formxpath='//form[@name="form1"]',
                formdata={'wd':c, 'sort':'8'},
                callback=self.parse_shufazidian
        )

    def parse_shufazidian(self, response):
        #with open('page.html','w', encoding='utf-8') as file_object:
        #    file_object.write(str(response.body, encoding='utf-8'))
        page = Selector(response)

        #srcs = page.xpath("//a[contains(@rel,'example_group')]/@href").extract()
        #print(srcs)
        #titles = page.xpath("//a[contains(@rel,'example_group')]/@title").extract()
        #print(titles)

        #print(page.xpath("/html/body/div[3]/div[2]/div[1]/div[2]/div").extract())
        for sel in page.xpath("/html/body/div[3]/div[2]/div[1]/div[2]/div"):
            item = ShufazidianItem()
            item['title'] = sel.xpath('div/div//text()').extract()[0]
            item['image_urls'] = [sel.xpath('div/div/a/img/@src').extract()[0]]
            item['category'] = sel.xpath('//form[@name="form1"]/input[@id="wd"]/@value').extract()[0]
            yield item
