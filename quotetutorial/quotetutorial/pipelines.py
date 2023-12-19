# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Scraped data -> Item Containers -> Json/csv files
# Scraped data -> Item Containers -> Pipeline -> Sql/Mongo database

import mysql.connector


class QuotetutorialPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='1610322133',
            database='myquotes'

        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_db""")
        self.curr.execute("""create table quotes_db(
                        title text,
                        author text,
                        tag text
                        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        print("pipeline : " + item["title"][0])
        return item

    def store_db(self, item):
        self.curr.execute("""insert into quotes_db values (%s, %s, %s)""", (
            item['title'][0],
            item['author'][0],
            item['tag'][0]
        ))
        self.conn.commit()

