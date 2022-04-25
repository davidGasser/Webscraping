# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime

def remove_quotes(text):
    text = text.strip(u'\u201c'u'\u201d')
    return text 

def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y')

def parse_location(text):
    return text[3:]

def pick_second(array):
    if array != " ":
        return array

class QuoteItem(scrapy.Item):
    quote_content = scrapy.Field(
        input_processor=MapCompose(remove_quotes),
        output_processor=TakeFirst()
        )
    tags = scrapy.Field()
    author_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    author_birthday = scrapy.Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
        )
    author_bornlocation = scrapy.Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()
        )
    author_bio = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )


class sightItem(scrapy.Item):
    sight_name = scrapy.Field(
        input_processor= MapCompose(pick_second),
        output_processor=TakeFirst()
        )
    sight_catagory=scrapy.Field(
        output_processor=TakeFirst()
        )
    sight_detail = scrapy.Field(
        output_processor=TakeFirst()
        )
    sight_address = scrapy.Field(
        input_processor= MapCompose(str.strip("]['")),
        output_processor=TakeFirst()
        )
    sight_duration = scrapy.Field(
        output_processor=TakeFirst()
        )
