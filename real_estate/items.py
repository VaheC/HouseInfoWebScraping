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
    # attributes = scrapy.Field()
    construction_type = scrapy.Field()
    new_construction = scrapy.Field()
    elevator = scrapy.Field()
    floors_in_the_building = scrapy.Field()
    the_house_has = scrapy.Field()
    parking = scrapy.Field()
    floor_area = scrapy.Field()
    number_of_rooms = scrapy.Field()
    number_of_bathrooms = scrapy.Field()
    ceiling_height = scrapy.Field()
    floor = scrapy.Field()
    balcony = scrapy.Field()
    furniture = scrapy.Field()
    renovation = scrapy.Field()
    appliances = scrapy.Field()
    window_views = scrapy.Field()
    estate_id = scrapy.Field()
