import scrapy
import re
from real_estate.items import RealEstateItem


class EstatespiderSpider(scrapy.Spider):
    name = "estatespider"
    allowed_domains = ["list.am"]
    start_urls = ["https://list.am/category/60"]

    # def parse(self, response):
    #     # temp_page_top_estate = response.css('div#tp')[0]
    #     # temp_page_top_estate = temp_page_top_estate.css('a.h')

    #     temp_page_top_estate = response.css('div.dl')[0].css('div.gl').css('a')
    #     temp_page_estate = response.css('div.dl')[1].css('div.gl').css('a')

    #     for i in range(len(temp_page_top_estate)):
    #         temp_estate = temp_page_top_estate[i]
    #         yield {
    #             'price': temp_estate.css('.p::text').get(),
    #             'desc1': temp_estate.css('.l::text').get(),
    #             'seller': temp_estate.css('.clabel::text').get(),
    #             'desc2': temp_estate.css('.at::text').get(),
    #             'url': temp_estate.css('a').attrib['href'],
    #             'image_src': response.xpath(f'//*[@id="tp"]/div[2]/div/a[{i+1}]/img/@src').extract()[0]
    #         }

    #     next_page = response.css('div.dlf').css('a')[-1].attrib['href']
    #     next_page_url = f"https://list.am{next_page}"
    #     if next_page_url is not None:
    #         yield response.follow(next_page_url, callback=self.parse)
# //*[@id="contentr"]/div[4]/div/a[34]/img
# //*[@id="tp"]/div[2]/div/a/img
# //*[@id="tp"]/div[2]/div/a[1]/img
# //*[@id="tp"]/div[2]/div/a[2]/img
# /html/body/div[3]/div[5]/div[2]/div[2]/div[2]/div/a[2]/img
# response.xpath('//*[@id="tp"]/div[2]/div/a[1]/img/@src').extract()[0]
            
# https://www.list.am/en/item/20733406
            
    def parse(self, response):

        temp_page_top_estate = response.css('div.dl')[0].css('div.gl').css('a')
        temp_page_estate = response.css('div.dl')[1].css('div.gl').css('a')

        estates_url_list = [temp_estate.css('a').attrib['href'] for temp_estate in temp_page_top_estate]
        estates_url_list.extend([temp_estate.css('a').attrib['href'] for temp_estate in temp_page_estate])

        for temp_rev_url in estates_url_list:
            temp_url = f"https://www.list.am/en{temp_rev_url}"
            yield scrapy.Request(temp_url, callback=self.parse_estate_page)

        next_page = response.css('div.dlf').css('a')[-1].attrib['href']
        next_page_url = f"https://list.am{next_page}"
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_estate_page(self, response):
        price_seller_list = response.css('div.price').css('span')

        try:
            description_text = re.findall(r'itemprop="description">(.*)<div', response.css('div.body').get())[0]
        except:
            description_text = None

        try:
            placesby_text = ', '.join([elem.css('td')[0].css('::text').get() for elem in response.css('table.poi')[0].css('tr')])
        except:
            placesby_text = None

        posted_date = response.css('div.footer span')[1].css('::text').get()
        renewed_date = response.css('div.footer span')[2].css('::text').get()

        # info_dict = {
        #     'address': response.css('div.loc a::text').get(),
        #     'price_usd': price_seller_list[2].css('::text').get(),
        #     'price_amd': price_seller_list[3].css('::text').get(),
        #     'price_rub': price_seller_list[4].css('::text').get(),
        #     'seller': price_seller_list[5].css('::text').get(),
        #     'seller_id': response.css('div#uinfo a').attrib['href'].split('/')[-1],
        #     'description': description_text,
        #     'placesby': placesby_text,
        #     'posted_date': posted_date,
        #     'renewed_date': renewed_date
        # }

        estate_attributes = response.css('div.attr.g')

        # for estate_attr in estate_attributes:
        #     temp_attr_dict = {
        #         elem.css('div.t::text').get(): elem.css('div.i::text').get() 
        #         for elem in estate_attr[0].css('div.c')
        #     }
        #     info_dict.update(temp_attr_dict)

        attributes_dict = {}
        for estate_attr in estate_attributes:
            temp_attr_dict = {
                elem.css('div.t::text').get(): elem.css('div.i::text').get()
                for elem in estate_attr.css('div.c')
            }
            attributes_dict.update(temp_attr_dict)

        estate_item = RealEstateItem()
        estate_item['address'] = response.css('div.loc a::text').get()
        estate_item['price_usd'] = price_seller_list[2].css('::text').get()
        estate_item['price_amd'] = price_seller_list[3].css('::text').get()
        estate_item['price_rub'] = price_seller_list[4].css('::text').get()
        estate_item['seller'] = price_seller_list[5].css('::text').get()
        estate_item['seller_id'] = response.css('div#uinfo a').attrib['href'].split('/')[-1]
        estate_item['description'] = description_text
        estate_item['placesby'] = placesby_text
        estate_item['posted_date'] = posted_date
        estate_item['renewed_date'] = renewed_date
        # estate_item['attributes'] = attributes_list
        estate_item['construction_type'] = attributes_dict.get('Construction Type', None)
        estate_item['new_construction'] = attributes_dict.get('New Construction', None)
        estate_item['elevator'] = attributes_dict.get('Elevator', None)
        estate_item['floors_in_the_building'] = attributes_dict.get('Floors in the Building', None)
        estate_item['the_house_has'] = attributes_dict.get('The House Has', None)
        estate_item['parking'] = attributes_dict.get('Parking', None)
        estate_item['floor_area'] = attributes_dict.get('Floor Area', None)
        estate_item['number_of_rooms'] = attributes_dict.get('Number of Rooms', None)
        estate_item['number_of_bathrooms'] = attributes_dict.get('Number of Bathrooms', None)
        estate_item['ceiling_height'] = attributes_dict.get('Ceiling Height', None)
        estate_item['floor'] = attributes_dict.get('Floor', None)
        estate_item['balcony'] = attributes_dict.get('Balcony', None)
        estate_item['furniture'] = attributes_dict.get('Furniture', None)
        estate_item['renovation'] = attributes_dict.get('Renovation', None)
        estate_item['appliances'] = attributes_dict.get('Appliances', None)
        estate_item['window_views'] = attributes_dict.get('Window Views', None)

        yield estate_item

        