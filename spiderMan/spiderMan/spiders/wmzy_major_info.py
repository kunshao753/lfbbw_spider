# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from spiderMan.items import MajorItem
from spiderMan.items import MajorDetailItem
from spiderMan.items import MajorEnrollItem
from spiderMan.items import enrollMajorSelectItem
from spiderMan.items import emEnrollDataItem
from spiderMan.items import emAdmDataItem
from spiderMan.items import emDetailItem
from spiderMan.items import CareerItem
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')


class WmzyMajorInfoSpider(scrapy.Spider):
    name = 'wmzy_major_info'
    allowed_domains = ['wmzy.com']
    start_urls = ['https://www.wmzy.com/gw/api/sku/sku_service/major_info_all?diploma_id=']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Channel': 'www.wmzy.com pc',
        'Content-Type': 'application/json; charset=utf-8',
    }

    login_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Channel': 'www.wmzy.com pc',
        'Content-Type': 'application/json; charset=utf-8',
        "Content-Type": "application/json",
        "Authorization": "4503446 Un8iZ/jMlpc518NfFEYMFG2ntSpp0aAKivue9EbaDfYLUoCrtTa7TGyAFs+NHCmP",
    }
    province_ids = {
        "650000000000", "640000000000", "630000000000", "620000000000", "610000000000", "530000000000", "520000000000",
    "510000000000", "500000000000", "460000000000", "450000000000", "440000000000", "430000000000", "420000000000",
    "410000000000", "370000000000", "360000000000", "350000000000", "340000000000", "330000000000", "320000000000",
    "310000000000", "230000000000", "220000000000", "210000000000", "150000000000", "140000000000", "130000000000",
    "120000000000", "110000000000"
    }

    # province_ids = {
    #     "650000000000", "640000000000", "630000000000", "620000000000", "610000000000", "530000000000", "520000000000",
    # "510000000000", "500000000000", "460000000000", "450000000000", "440000000000", "430000000000", "420000000000",
    # "410000000000", "370000000000", "360000000000", "350000000000", "340000000000", "330000000000", "320000000000",
    # "310000000000", "230000000000", "220000000000", "210000000000", "150000000000", "140000000000",
    # "120000000000", "110000000000"
    # }

    # province_ids = {
    #     "110000000000"
    # }
    def start_requests(self):
        # 7:本科  5：专科
        diplomas = ['7', '5']
        for diploma in diplomas:
            url = self.start_urls[0] + diploma
            meta = {
                "diploma": diploma
            }
            request = Request(url, meta=meta, callback=self.parse, method='GET', headers=self.headers)
            yield request

    def parse(self, response):
        _meta = response.meta
        json_content = json.loads(response.body)
        if json_content['code'] == 0:
            major_item = MajorItem()
            for data in json_content['data']['subjects']:
                sid = data['sid']
                sname = data['sname']
                categories = data['categories']
                for categorie in categories:
                    cid = categorie['cid']
                    cname = categorie['cname']
                    majors = categorie['majors']
                    for major in majors:
                        mid = major['mid']
                        mname = major['mname']

                        major_item['diploma'] = _meta['diploma']
                        major_item['sid'] = sid
                        major_item['sname'] = sname
                        major_item['cid'] = cid
                        major_item['cname'] = cname
                        major_item['mid'] = mid
                        major_item['mname'] = mname
                        major_item['t'] = 'major'
                        # yield major_item

                        # ========构造详情页的请求=========
                        # detail_url = "https://www.wmzy.com/gw/api/sku/sku_service/major_detail_info?major_id=" + mid
                        # yield scrapy.Request(detail_url, headers=self.headers, callback=self.parse_detail_page)

                        # ========专业注册单元========
                        major_enroll_unit_url = "https://www.wmzy.com/gw/api/sku/enroll_admission_service/major_enroll_unit"
                        wen_li_flags = {1, 2}
                        for wen_li in wen_li_flags:
                            for province in self.province_ids:
                                form_data = {
                                    "page": 1,
                                    "page_size": 200,
                                    "stu_province_id": province,
                                    "major_id": mid,
                                    "enroll_category": 1,
                                    "enroll_mode": 1,
                                    "sch_filter": {

                                    },
                                    "wenli": wen_li,
                                }
                                meta = {
                                    "mid": mid,
                                    "wen_li": wen_li,
                                    "major_id": mid,
                                    "diploma": _meta['diploma'],
                                    "stu_province_id": province
                                }
                                yield scrapy.Request(major_enroll_unit_url, meta=meta, callback=self.parse_major_enroll_info,
                                                     method='POST', headers=self.headers, body=json.dumps(form_data))

    def parse_detail_page(self, response):
        json_content = json.loads(response.body)
        if json_content['code'] == 0:
            major_detail_item = MajorDetailItem()
            data = json_content['data']
            major_detail_item['mid'] = data['mid']
            major_detail_item['intro'] = data['intro']
            major_detail_item['academic_rule'] = data['academic_rule']
            major_detail_item['degree'] = data['degree']
            major_detail_item['training_objective'] = data['training_objective']
            major_detail_item['training_requirement'] = data['training_requirement']
            major_detail_item['employment_info'] = data['employment_info']
            major_detail_item['main_course'] = data['main_course']
            major_detail_item['knowledge_requirement'] = data['knowledge_requirement']
            major_detail_item['teaching_practice'] = data['teaching_practice']
            major_detail_item['t'] = 'major_detail'
            #yield major_detail_item

            try:
                if len(data['careers']) > 0:
                    career_item = CareerItem()
                    for career in data['careers']:
                        career_item['career_id'] = career['id']
                        career_item['name'] = career['name']
                        career_item['desc'] = career['desc']
                        career_item['t'] = 'career'
                        # yield career_item
            except (IndexError, BaseException):
                print('不存在career')

    def parse_major_enroll_info(self, response):
        enroll_major_select_url = "https://www.wmzy.com/gw/enroll_admission_service/enroll_major_select"
        _meta = response.meta
        major_enroll_item = MajorEnrollItem()
        json_content = json.loads(response.body)
        if json_content['code'] == 0 and json_content['data']['total'] > 0:
            for enroll_units in json_content['data']['enroll_units']:
                major_enroll_item['mid'] = _meta['mid']
                major_enroll_item['wenli'] = _meta['wen_li']
                major_enroll_item['sch_id'] = enroll_units['sch_id']
                major_enroll_item['province_id'] = enroll_units['province_id']
                major_enroll_item['city_id'] = enroll_units['city_id']
                major_enroll_item['city_id_desc'] = enroll_units['city_id_desc']
                major_enroll_item['eu_code'] = enroll_units['eu_code']
                major_enroll_item['stu_province_id'] = _meta['stu_province_id']

                major_enroll_item['diploma_desc'] = enroll_units['diploma_desc']
                major_enroll_item['diploma_id'] = enroll_units['diploma_id']
                major_enroll_item['enroll_group_no'] = enroll_units['enroll_group_no']
                major_enroll_item['eu_id'] = enroll_units['eu_id']
                major_enroll_item['eu_name'] = enroll_units['eu_name']
                major_enroll_item['has_grad_sch'] = enroll_units['has_grad_sch']
                major_enroll_item['independent_college'] = enroll_units['independent_college']
                major_enroll_item['major_diploma_id'] = enroll_units['major_diploma_id']
                major_enroll_item['province_id_desc'] = enroll_units['province_id_desc']
                major_enroll_item['required_course_desc'] = '_'.join(enroll_units['required_course_desc'])
                major_enroll_item['required_course_num'] = enroll_units['required_course_num']

                major_enroll_item['t'] = 'major_enroll'
                yield major_enroll_item

                form_data = {
                    "stu_province_id": enroll_units['province_id'],
                    "enroll_unit_id": enroll_units['sch_id'],
                    "major_id": _meta['major_id'],
                    "enroll_admission_dimension": {
                        "enroll_category": 1,
                        "enroll_mode": 1,
                        "diploma_id": int(_meta['diploma']),
                        "wenli": int(_meta['wen_li'])
                    }
                }
                meta = {
                    "major_id": _meta['major_id'],
                    "province_id": enroll_units['province_id'],
                    "sch_id": enroll_units['sch_id']
                }
                # yield scrapy.Request(enroll_major_select_url, meta=meta, callback=self.parse_enroll_major_select,
                #                      method='POST', headers=self.headers, body=json.dumps(form_data))

    def parse_enroll_major_select(self, response):
        em_enroll_data_url = "https://www.wmzy.com/gw/enroll_admission_service/em_enroll_data_in_eu"
        # 专业招生计划
        em_detail_url = "https://www.wmzy.com/gw/enroll_admission_service/em_detail_in_eu"
        # 专业录取数据
        em_adm_data_url = "https://www.wmzy.com/gw/enroll_admission_service/em_adm_data_in_eu"
        enroll_major_select_item = enrollMajorSelectItem()
        _meta = response.meta
        json_content = json.loads(response.body)
        if json_content['code'] == 0 and json_content['data']['total'] > 0:
            for enroll_major_select in json_content['data']['record']:
                enroll_major_select_item['batch'] = enroll_major_select['batch']
                enroll_major_select_item['batch_ex'] = enroll_major_select['batch_ex']
                enroll_major_select_item['batch_name'] = enroll_major_select['batch_name']
                enroll_major_select_item['diploma_id'] = enroll_major_select['diploma_id']
                enroll_major_select_item['enroll_major_code'] = enroll_major_select['enroll_major_code']
                enroll_major_select_item['enroll_major_id'] = enroll_major_select['enroll_major_id']
                enroll_major_select_item['enroll_major_name'] = enroll_major_select['enroll_major_name']
                enroll_major_select_item['enroll_stage'] = enroll_major_select['enroll_stage']
                enroll_major_select_item['enroll_unit_id'] = enroll_major_select['enroll_unit_id']
                enroll_major_select_item['major_diploma_id'] = enroll_major_select['major_diploma_id']
                enroll_major_select_item['wenli'] = enroll_major_select['wenli']
                enroll_major_select_item['t'] = 'enroll_major_select'
                yield enroll_major_select_item

                form_data = {
                    "enroll_unit_id": enroll_major_select['enroll_unit_id'],
                    "enroll_major_id": _meta['major_id'],
                    "wenli": enroll_major_select['wenli'],
                    "diploma_id": enroll_major_select['diploma_id'],
                    "batch": enroll_major_select['batch'],
                    "batch_ex": enroll_major_select['batch_ex'],
                    "enroll_stage": enroll_major_select['enroll_stage'],
                    "major_diploma_id": enroll_major_select['major_diploma_id'],
                    "page_from": "major_sku",
                    "enroll_category": 1,
                    "enroll_mode": 1,
                    "stu_id": "",
                    "stu_province_id": _meta['province_id']
                }
                meta = {
                    "province_id": _meta['province_id'],
                    "major_id": _meta['major_id'],
                    "enroll_major_id": _meta['major_id'],
                    "diploma_id": enroll_major_select['diploma_id'],
                    "major_diploma_id": enroll_major_select['major_diploma_id'],
                    "wenli": enroll_major_select['wenli'],
                    "sch_id": _meta['sch_id']
                }
                yield scrapy.Request(em_enroll_data_url, meta=meta, callback=self.parse_em_enroll_data,
                                     method='POST', headers=self.headers, body=json.dumps(form_data))
                yield scrapy.Request(em_detail_url, meta=meta, callback=self.parse_em_detail,
                                     method='POST', headers=self.headers, body=json.dumps(form_data))
                yield scrapy.Request(em_adm_data_url, meta=meta, callback=self.parse_em_adm_data,
                                     method='POST', headers=self.headers, body=json.dumps(form_data))
    # 专业招生计划
    def parse_em_enroll_data(self, response):
        _meta = response.meta
        em_enroll_data_item = emEnrollDataItem()
        json_content = json.loads(response.body)
        if json_content['code'] == 0 \
                and 'em_enroll_data' in json_content['data'].keys() \
                and json_content['data']['em_enroll_data'] > 0:
            for em_enroll_data in json_content['data']['em_enroll_data']:
                em_enroll_data_item['academic_rule'] = em_enroll_data['academic_rule']
                em_enroll_data_item['academic_year'] = em_enroll_data['academic_year']
                em_enroll_data_item['batch_name'] = em_enroll_data['batch_name']
                em_enroll_data_item['enroll_plan_count'] = em_enroll_data['enroll_plan_count']
                em_enroll_data_item['tuition'] = em_enroll_data['tuition']

                em_enroll_data_item['major_id'] = _meta['major_id']
                em_enroll_data_item['enroll_major_id'] = _meta['enroll_major_id']
                em_enroll_data_item['sch_id'] = _meta['sch_id']
                em_enroll_data_item['diploma_id'] = _meta['diploma_id']
                em_enroll_data_item['major_diploma_id'] = _meta['major_diploma_id']
                em_enroll_data_item['wenli'] = _meta['wenli']
                em_enroll_data_item['province_id'] = _meta['province_id']

                em_enroll_data_item['t'] = 'em_enroll_data'
                yield em_enroll_data_item

    def parse_em_detail(self, response):
        em_detail_item = emDetailItem()
        json_content = json.loads(response.body)
        if json_content['code'] == 0 and json_content['data']['enroll_major_id'] != "":
            em_detail = json_content['data']
            em_detail_item['batch_name'] = em_detail['batch_name']
            em_detail_item['diploma_id'] = em_detail['diploma_id']
            em_detail_item['enroll_group_no'] = em_detail['enroll_group_no']
            em_detail_item['enroll_major_code'] = em_detail['enroll_major_code']
            em_detail_item['enroll_major_id'] = em_detail['enroll_major_id']
            em_detail_item['enroll_major_name'] = em_detail['enroll_major_name']
            em_detail_item['enroll_unit_code'] = em_detail['enroll_unit_code']
            em_detail_item['enroll_unit_id'] = em_detail['enroll_unit_id']
            em_detail_item['enroll_unit_name'] = em_detail['enroll_unit_name']
            em_detail_item['major_id'] = em_detail['major_id']
            em_detail_item['major_logo'] = em_detail['major_logo']
            em_detail_item['major_teach_location'] = em_detail['major_teach_location']
            em_detail_item['ncee_type'] = em_detail['ncee_type']
            em_detail_item['optional_course_desc'] = em_detail['optional_course_desc']
            em_detail_item['optional_course_level'] = em_detail['optional_course_level']
            em_detail_item['require_language'] = em_detail['require_language']
            em_detail_item['required_course_desc'] = em_detail['required_course_desc']
            em_detail_item['required_course_level'] = em_detail['required_course_level']
            em_detail_item['required_course_num'] = em_detail['required_course_num']
            em_detail_item['sch_id'] = em_detail['sch_id']
            em_detail_item['wenli'] = em_detail['wenli']
            em_detail_item['t'] = 'em_detail'
            yield em_detail_item

    # 专业录取数据
    def parse_em_adm_data(self, response):
        _meta = response.meta
        em_adm_data_item = emAdmDataItem()
        json_content = json.loads(response.body)
        if json_content['code'] == 0 \
                and 'em_adm_data' in json_content['data'].keys() \
                and json_content['data']['em_adm_data'] > 0:
            for em_adm_data in json_content['data']['em_adm_data']:
                em_adm_data_item['academic_year'] = em_adm_data['academic_year']
                em_adm_data_item['admission_count'] = em_adm_data['admission_count']
                em_adm_data_item['avg_score'] = em_adm_data['avg_score']
                em_adm_data_item['avg_score_rank'] = em_adm_data['avg_score_rank']
                em_adm_data_item['batch'] = em_adm_data['batch']
                em_adm_data_item['batch_ex'] = em_adm_data['batch_ex']
                em_adm_data_item['batch_name'] = em_adm_data['batch_name']
                em_adm_data_item['enroll_group_no'] = em_adm_data['enroll_group_no']
                em_adm_data_item['max_score'] = em_adm_data['max_score']
                em_adm_data_item['max_score_rank'] = em_adm_data['max_score_rank']
                em_adm_data_item['min_score'] = em_adm_data['min_score']
                em_adm_data_item['min_score_diff'] = em_adm_data['min_score_diff']
                em_adm_data_item['min_score_rank'] = em_adm_data['min_score_rank']

                em_adm_data_item['major_id'] = _meta['major_id']
                em_adm_data_item['enroll_major_id'] = _meta['enroll_major_id']
                em_adm_data_item['sch_id'] = _meta['sch_id']
                em_adm_data_item['diploma_id'] = _meta['diploma_id']
                em_adm_data_item['major_diploma_id'] = _meta['major_diploma_id']
                em_adm_data_item['wenli'] = _meta['wenli']
                em_adm_data_item['province_id'] = _meta['province_id']

                em_adm_data_item['t'] = 'em_adm_data'

                print("-----------")
                print(em_adm_data_item)
                print("-----------")

                yield em_adm_data_item
