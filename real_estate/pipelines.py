# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime as dt


class RealEstatePipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        value = adapter.get('price_usd')
        adapter['price_usd'] = int(value.replace('$', '').replace(',', '').strip())

        value = adapter.get('price_amd')
        adapter['price_amd'] = int(value.replace('֏', '').replace(',', '').strip())

        value = adapter.get('price_rub')
        adapter['price_rub'] = int(value.replace('₽', '').replace(',', '').strip())

        for field_name in ['address', 'placesby_text', 'seller_id', 'seller']:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        value = adapter.get('description_text')
        adapter['description_text'] = value.replace('<br>', '\n').strip()

        for field_name in ['posted_date', 'renewed_date']:
            temp_replace_value = field_name.split('_')[0].capitalize()
            value = adapter.get(field_name)
            adapter[field_name] = dt.strptime(
                '-'.join(value.replace(f'{temp_replace_value} ', '').strip().split(' ')[0].split('.')[::-1]), 
                '%Y-%m-%d'
            )

        return item
