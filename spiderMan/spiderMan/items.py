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


# 专业信息
class MajorItem(scrapy.Item):
    sid = Field()
    sname = Field()
    cid = Field()
    cname = Field()
    mid = Field()
    mname = Field()
    diploma = Field()
    t = Field()


# 专业详细信息
class MajorDetailItem(scrapy.Item):
    mid = Field()
    intro = Field()
    academic_rule = Field()
    degree = Field()
    training_objective = Field()
    training_requirement = Field()
    employment_info = Field()
    main_course = Field()
    knowledge_requirement = Field()
    teaching_practice = Field()
    t = Field()


# 专业详细信息
class CareerItem(scrapy.Item):
    mid = Field()
    career_id = Field()
    name = Field()
    desc = Field()
    t = Field()


# 注册专业信息
class MajorEnrollItem(scrapy.Item):
    mid = Field()
    wenli = Field()
    sch_id = Field()
    province_id = Field()
    city_id = Field()
    city_id_desc = Field()
    eu_code = Field()
    stu_province_id = Field()

    diploma_desc = Field()
    diploma_id = Field()
    enroll_group_no = Field()
    eu_id = Field()
    eu_name = Field()
    has_grad_sch = Field()
    independent_college = Field()
    major_diploma_id = Field()
    province_id_desc = Field()
    required_course_desc = Field()
    required_course_num = Field()

    t = Field()


#
class enrollMajorSelectItem(scrapy.Item):
    batch = Field()
    batch_ex = Field()
    batch_name = Field()
    diploma_id = Field()
    enroll_major_code = Field()
    enroll_major_id = Field()
    enroll_major_name = Field()
    enroll_stage = Field()
    enroll_unit_id = Field()
    major_diploma_id = Field()
    wenli = Field()

    t = Field()

 # 专业招生计划
class emEnrollDataItem(scrapy.Item):
    academic_rule = Field()
    academic_year = Field()
    batch_name = Field()
    enroll_plan_count = Field()
    tuition = Field()

    sch_id = Field()
    major_id = Field()
    enroll_major_id = Field()
    diploma_id = Field()
    major_diploma_id = Field()
    wenli = Field()
    province_id = Field()

    t = Field()

# 专业录取数据
class emAdmDataItem(scrapy.Item):
    academic_year = Field()
    admission_count = Field()
    avg_score = Field()
    avg_score_rank = Field()
    batch = Field()
    batch_ex = Field()
    batch_name = Field()
    enroll_group_no = Field()
    max_score = Field()
    max_score_rank = Field()
    min_score = Field()
    min_score_diff = Field()
    min_score_rank = Field()

    sch_id = Field()
    major_id = Field()
    enroll_major_id = Field()
    diploma_id = Field()
    major_diploma_id = Field()
    wenli = Field()
    province_id = Field()

    t = Field()


class emDetailItem(scrapy.Item):
    batch_name = Field()
    diploma_id = Field()
    enroll_group_no = Field()
    enroll_major_code = Field()
    enroll_major_id = Field()
    enroll_major_name = Field()
    enroll_unit_code = Field()
    enroll_unit_id = Field()
    enroll_unit_name = Field()
    major_id = Field()
    major_logo = Field()
    major_teach_location = Field()
    ncee_type = Field()
    optional_course_desc = Field()
    optional_course_level = Field()
    require_language = Field()
    required_course_desc = Field()
    required_course_level = Field()
    required_course_num = Field()
    sch_id = Field()
    wenli = Field()
    t = Field()


# enroll unit
class EnrollUnitListItem(scrapy.Item):
    enroll_unit_code = Field()
    enroll_unit_id = Field()
    enroll_unit_name = Field()
    stu_province_id = Field()
    sch_id = Field()
    t = Field()


# enroll rule
class EnrollRuleInfoItem(scrapy.Item):
    sch_id = Field()
    academic_year = Field()
    enroll_rule_title = Field()
    content = Field()
    t = Field()


# sch info ext
class SchInfoExtItem(scrapy.Item):
    province_id = Field()
    latest_admission_year = Field()
    latest_enroll_year = Field()
    city_id = Field()
    city_id_desc = Field()
    region_id = Field()
    regioin_id_desc = Field()
    sch_code = Field()
    nation_id = Field()
    sch_id = Field()
    t = Field()