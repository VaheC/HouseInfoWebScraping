import scrapy
import re
from real_estate.items import RealEstateItem


class EstatespiderSpider(scrapy.Spider):
    name = "estatespider"
    allowed_domains = ["list.am"]
    start_urls = ["https://list.am/en/category/60"]

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
        
        # temp_page_top_estate = response.css('div#tp')[0]
        temp_page_top_estate = response.css('div.dl')[0].css('div.gl').css('a')
        temp_page_estate = response.css('div.dl')[1].css('div.gl').css('a')

        estates_url_list = [temp_estate.css('a').attrib['href'] for temp_estate in temp_page_top_estate]
        estates_url_list.extend([temp_estate.css('a').attrib['href'] for temp_estate in temp_page_estate])
        # estates_url_list.extend([temp_estate.css('a').attrib['href'] for temp_estate in temp_page_top_estate2])
        # estates_url_list = list(set(estates_url_list))

        for temp_rev_url in estates_url_list:
            # if temp_rev_url.split('/')[1] != 'en':
            temp_url = f"https://www.list.am{temp_rev_url}"
            yield scrapy.Request(temp_url, callback=self.parse_estate_page)

        # next_page = response.css('div.dlf').css('a')[-1].attrib['href']
        # next_page_url = f"https://list.am{next_page}"
        # if next_page_url is not None:
        #     yield response.follow(next_page_url, callback=self.parse)

    def parse_estate_page(self, response):
        price_seller_list = response.css('div.price').css('span')

        try:
            description_text = re.findall(r'itemprop="description">(.*)<div', response.css('div.body').get())[0]
        except:
            description_text = "Unknown"

        try:
            placesby_text = ', '.join([elem.css('td')[0].css('::text').get() for elem in response.css('table.poi')[0].css('tr')])
        except:
            placesby_text = "Unknown"

        estate_id_text = response.css('div.footer span')[0].css('::text').get()
        posted_date = response.css('div.footer span')[1].css('::text').get()

        try:
            renewed_date = response.css('div.footer span')[2].css('::text').get()
        except:
            renewed_date = "Renewed 31.12.1979 00:00"

        try:
            address_text = response.css('div.loc a::text').get()
        except:
            address_text = "Unknown"

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

        attribute_arm2eng_dict = {
            'Շինության տիպ': 'Construction Type',
            'Նորակառույց': 'New Construction',
            'Վերելակ': 'Elevator',
            'Հարկերի քանակ': 'Floors in the Building',
            'Առկա են': 'The House Has',
            'Կայանատեղի': 'Parking',
            'Ընդհանուր մակերես': 'Floor Area',
            'Սենյակների քանակ': 'Number of Rooms',
            'Սանհանգույցների քանակ': 'Number of Bathrooms',
            'Առաստաղի բարձրություն': 'Ceiling Height',
            'Հարկ': 'Floor',
            'Պատշգամբ': 'Balcony',
            'Կահույք': 'Furniture',
            'Վերանորոգում': 'Renovation',
            'Տեսարաններ պատուհաններից': 'Window Views',
        }

        attributes_dict = {}
        for estate_attr in estate_attributes:
            temp_attr_dict = {
                attribute_arm2eng_dict.get(
                    elem.css('div.t::text').get(), 
                    elem.css('div.t::text').get()
                ): elem.css('div.i::text').get()
                for elem in estate_attr.css('div.c')
            }
            attributes_dict.update(temp_attr_dict)

        temp_attr_dict = {elem.css('div.t::text').get(): elem.css('div.i::text').get() for elem in estate_attributes[0].css('div.c')}

        estate_item = RealEstateItem()
        estate_item['address'] = address_text
        estate_item['price_usd'] = price_seller_list[2].css('::text').get()
        estate_item['price_amd'] = price_seller_list[3].css('::text').get()
        estate_item['price_rub'] = price_seller_list[4].css('::text').get()

        try:
            estate_item['seller'] = price_seller_list[5].css('::text').get()
        except:
            estate_item['seller'] = 'Unknown'

        estate_item['seller_id'] = response.css('div#uinfo a').attrib['href'].split('/')[-1]
        estate_item['description'] = description_text
        estate_item['placesby'] = placesby_text
        estate_item['posted_date'] = posted_date
        estate_item['renewed_date'] = renewed_date
        # estate_item['attributes'] = attributes_list
        estate_item['construction_type'] = attributes_dict.get('Construction Type', "Unknown")
        estate_item['new_construction'] = attributes_dict.get('New Construction', "Unknown")
        estate_item['elevator'] = attributes_dict.get('Elevator', "Unknown")
        estate_item['floors_in_the_building'] = attributes_dict.get('Floors in the Building', "Unknown")
        estate_item['the_house_has'] = attributes_dict.get('The House Has', "Unknown")
        estate_item['parking'] = attributes_dict.get('Parking', "Unknown")
        estate_item['floor_area'] = attributes_dict.get('Floor Area', "Unknown")
        estate_item['number_of_rooms'] = attributes_dict.get('Number of Rooms', "Unknown")
        estate_item['number_of_bathrooms'] = attributes_dict.get('Number of Bathrooms', "Unknown")
        estate_item['ceiling_height'] = attributes_dict.get('Ceiling Height', "Unknown")
        estate_item['floor'] = attributes_dict.get('Floor', "Unknown")
        estate_item['balcony'] = attributes_dict.get('Balcony', "Unknown")
        estate_item['furniture'] = attributes_dict.get('Furniture', "Unknown")
        estate_item['renovation'] = attributes_dict.get('Renovation', "Unknown")
        estate_item['appliances'] = attributes_dict.get('Appliances', "Unknown")
        estate_item['window_views'] = attributes_dict.get('Window Views', "Unknown")
        estate_item['estate_id'] = estate_id_text

        yield estate_item

        