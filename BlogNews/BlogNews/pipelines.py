# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
import pymysql
import copy

class BlognewsPipeline:
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod   # 函数名固定 会被scrapy 调用 直接使用settings的值
    def from_settings(cls,settings):
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )


        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)


    def do_insert(self,cursor,item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
                insert into blog_news(title, summary, new_url, pub_time) VALUES (%s,%s,%s,%s)
                """
        cursor.execute(insert_sql,(item['title'],item['new_summary'],item['new_url'],item['pub_time']))

    def handle_error(self,failure):
        print(failure)

    def process_item(self, item, spider):

        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """

        #对象拷贝   深拷贝
        asynItem = copy.deepcopy(item)    #需要导入import copy

        query = self.dbpool.runInteraction(self.do_insert, asynItem)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常
        return item
