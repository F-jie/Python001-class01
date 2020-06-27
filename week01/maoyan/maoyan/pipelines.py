# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

class MaoyanPipeline:

    def process_item(self, item, spider):
        print('**********SAVING*********')
        my_dict = dict()
        my_dict['name'] = item['name']
        my_dict['type_m'] = item['type_m']
        my_dict['time'] = item['time']
        df = pd.DataFrame([my_dict], columns=['name', 'type_m', 'time'])
        df.to_csv('./data.csv', mode='a', encoding='utf8', index=False, header=False)
        return item
