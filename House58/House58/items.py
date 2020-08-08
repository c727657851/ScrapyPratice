# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class House58Item(scrapy.Item):
    # define the fields for your item here like:
    house_url = scrapy.Field()
    room_type = scrapy.Field()
    room_address = scrapy.Field()
    contact_person = scrapy.Field()
    money = scrapy.Field()
