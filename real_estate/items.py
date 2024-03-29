# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:
    address = scrapy.Field()
    price_usd = scrapy.Field()
    price_amd = scrapy.Field()
    price_rub = scrapy.Field()
    seller = scrapy.Field()
    seller_id = scrapy.Field()
    description = scrapy.Field()
    placesby = scrapy.Field()
    posted_date = scrapy.Field()
    renewed_date = scrapy.Field()
    attributes = scrapy.Field()
