import scrapy
from ..items import House58Item
import re
import base64
import io
from lxml import etree
from fontTools.ttLib import TTFont

class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['bj.58.com']
    start_urls = ['https://bj.58.com/chuzu/pn1/?PGTID=0d200001-0000-12f7-f36a-fe8f685abc7d&ClickID=1']
    base = '?PGTID=0d200001-0000-12f7-f36a-fe8f685abc7d&ClickID=1'

    def parse(self, response):
        text = response.text   # 用于清洗数据
        html = self.decode_data(text)
        html = etree.HTML(html)
        houses = html.xpath('//ul[@class="house-list"]//li')
        for house in houses:
            """
            house_url:  房子的详细信息
            room_type :  房子的户型
            room_address : 房子的地址
            contact_person : 房子的联系人
            money :  房子的价格

            """
            house_url = house.xpath('.//div[@class="des"]/h2/a/@href')
            print(house_url)
            room_type = house.xpath('.//div[@class="des"]/p[@class="room"]/text()')
            room_address = house.xpath('.//div[@class="des"]/p[@class="infor"]//text()')
            room_address = " ".join(room_address).strip()
            contact_person = house.xpath('.//div[@class="des"]/div[@class="jjr"]//text()')
            contact_person = " ".join(contact_person).strip()
            money = house.xpath('.//div[@class="money"]//text()')
            money = "".join(money).strip()
            item = House58Item(house_url=house_url,room_type=room_type,room_address=room_address,
                               contact_person=contact_person,money=money)
            yield item

        next_url = response.xpath('//a[@class="next"]/@href').get()
        if not next_url:
            return
        else:
            yield scrapy.Request(next_url+self.base, callback=self.parse)

    # 清洗数据  解决字体反爬的问题
    def decode_data(self,text):
        baseFont = TTFont('E:/Data/PycharmData/practice/House58/House58/spiders/zufang.ttf')
        # baseFont.saveXML('58zufang.xml')
        baseGlyf = baseFont['glyf']  # 当前页面的字体形状

        # 字体形状 -> 文字内容
        baseFontMap = {
            0: baseGlyf['glyph00001'],
            1: baseGlyf['glyph00002'],
            2: baseGlyf['glyph00003'],
            3: baseGlyf['glyph00004'],
            4: baseGlyf['glyph00005'],
            5: baseGlyf['glyph00006'],
            6: baseGlyf['glyph00007'],
            7: baseGlyf['glyph00008'],
            8: baseGlyf['glyph00009'],
            9: baseGlyf['glyph00010'],
        }
        result = re.search(
            r"font-family:'fangchan-secret';src:url\('data:application/font-ttf;charset=utf-8;base64,(.+?)'\)", text)
        font_face = result.group(1)

        b = base64.b64decode(font_face)

        currentFont = TTFont(io.BytesIO(b))
        currentGlyf = currentFont['glyf']

        currentCodeName = currentFont.getBestCmap()

        for code, name in currentCodeName.items():
            currentShape = currentGlyf[name]

            for number, shape in baseFontMap.items():
                if shape == currentShape:
                    webcode = str(hex(code)+';').replace('0', '&#', 1)
                    text = re.sub(webcode, str(number), text)
        return text

