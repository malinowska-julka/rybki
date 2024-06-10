# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class RybkaItem(Item):
    name = Field()
    latin_name = Field()
    temperature = Field()
    length = Field()
    from_where = Field()
    food_info = Field()
    akwarium_info = Field()  # rodzaj kryjowki
    breeding_info = Field()
    link_to_details = Field()
pass