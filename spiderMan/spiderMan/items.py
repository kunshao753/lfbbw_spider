# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


# 基础信息
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


# 详细信息
class DetailInfoItem(scrapy.Item):
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


# 知名校友
class CelebrityInfoItem(scrapy.Item):
    sch_id = Field()
    celebrity_name = Field()
    celebrity_desc = Field()
    t = Field()


# 重点学科
class DisciplineEvaluationItem(scrapy.Item):
    sch_id = Field()
    obj_id = Field()
    obj_name = Field()
    obj_num = Field()
    obj_list = Field()
    t = Field()


# 特色培养
class LibEvaluationItem(scrapy.Item):
    sch_id = Field()
    obj_id = Field()
    obj_name = Field()
    obj_num = Field()
    obj_list = Field()
    t = Field()