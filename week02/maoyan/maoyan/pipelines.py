# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class MaoyanPipeline:

    def process_item(self, item, spider):
        name = item['name']
        type_m = item['type_m']
        time = item['time']
        data = (name, type_m, time)
        print(data)
        save_data2sql(data)


def save_data2sql(data):
    connection = pymysql.connect('localhost', 'root', '6214', 'MAOYAN', charset='utf8', port=3306)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM movieInfo"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)

        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO movieInfo (name, type, onDate)  VALUES (%s, %s, %s)"
            cursor.execute(sql, (data[0], data[1], data[2]))
            connection.commit()
    except:
        print("There")
        connection.rollback()
    finally:
        connection.close()
