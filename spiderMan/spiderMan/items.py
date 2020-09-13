# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class SpiderManItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sch_id = Field()
    name = Field()
    english_name = Field()
    logo = Field()
    diploma = Field()
    run_type = Field()
    type = Field()
    tag = Field()
    grad = Field()
    location = Field()
    competent = Field()
    create_year = Field()
    province = Field()
    t = Field()


class DetailInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sch_faculty_info = Field()
    sch_id = Field()
    sch_intro = Field()
    sch_address = Field()
    sch_tel_num = Field()
    sch_female_ratio = Field()
    sch_master_ratio = Field()
    sch_abroad_ratio = Field()
    sch_scholarship = Field()
    sch_fellowship = Field()
    canteen_desc = Field()
    stu_dorm_desc = Field()
    t = Field()
