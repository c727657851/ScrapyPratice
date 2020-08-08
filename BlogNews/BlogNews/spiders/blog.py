import scrapy
from ..items import BlognewsItem

class BlogSpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/news/']

    def parse(self, response):
        post_lists = response.xpath('//div[@class="post-list"]/article')
        for post_list in post_lists:
            title = post_list.xpath('.//a[@class="post-item-title"]/text()').get()
            url = post_list.xpath('.//a[@class="post-item-title"]/@href').get()
            new_url = 'https:' + url
            new_summary = post_list.xpath('.//p[@class="post-item-summary"]/text()').getall()
            new_summary = "".join(new_summary).strip()  # 缩略内容
            pub_time = post_list.xpath('.//footer/span//text()').getall()
            pub_time = "".join(pub_time).strip()
            item = BlognewsItem(
                title=title,
                new_url=new_url,
                new_summary=new_summary,
                pub_time=pub_time
            )
            yield item

