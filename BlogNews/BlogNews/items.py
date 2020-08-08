# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlognewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    new_url = scrapy.Field()
    new_summary = scrapy.Field()
    pub_time = scrapy.Field()


