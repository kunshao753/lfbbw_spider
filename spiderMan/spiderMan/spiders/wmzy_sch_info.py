# coding=utf-8
import scrapy
from scrapy.http import Request
from spiderMan.items import SpiderManItem
from spiderMan.items import DetailInfoItem
from spiderMan.items import CelebrityInfoItem
from spiderMan.items import DisciplineEvaluationItem
from spiderMan.items import LibEvaluationItem
from spiderMan.items import EnrollUnitListItem
from spiderMan.items import EnrollRuleInfoItem
from spiderMan.items import SchInfoExtItem
from spiderMan.items import SchEnrollDataItem
from spiderMan.items import MajorEnrollDataItem
from spiderMan.items import MajorEnrollExtDataItem
import sys
import json
import re
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class WmzySchInfoSpider(scrapy.Spider):
    name = 'wmzy_sch_info'
    allowed_domains = ['wmzy.com']
    start_url = 'https://www.wmzy.com/gw/api/sku/sku_service/sch_complete'
    # ======录取招生页请求url start======
    get_enroll_unit_list_url = "https://www.wmzy.com/gw/api/sku/enroll_admission_service/get_enroll_unit_list"
    get_sch_enroll_rule_info_url = "https://www.wmzy.com/gw/sys/get_sch_enroll_rule_info"
    sch_enroll_data_url = "https://www.wmzy.com/gw/api/sku/enroll_admission_service/sch_enroll_data"
    # ======录取招生页请求url end  ======

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Channel': 'www.wmzy.com pc',
        'Content-Type': 'application/json; charset=utf-8',
    }

    # 默认情况下，scrapy都是采用GET请求。重写的目的：初始URL的请求修改用POST请求。
    # 需要重写start_requests()方法。
    def start_requests(self):

        # 142页
        for page_num in range(1, 143):
            form_data = {
                "filter": {},
                "page": page_num,
                "page_size": 20
            }
            # FormRequest()就是用来构造POST请求的类。
            request = Request(self.start_url, callback=self.parse, method='POST', headers=self.headers, body=json.dumps(form_data))
            yield request

    def parse(self, response):
        json_content = json.loads(response.body)
        # print(json_content['data'])
        item = SpiderManItem()
        for data in json_content['data']['sch_short_info']:
            sch_id = data['sch_id']
            diploma_desc = data['diploma_desc']
            grad_desc = data['grad_desc']
            province = data['location']
            location = data['province']
            sch_competent_desc = data['sch_competent_desc']
            sch_create_time = data['sch_create_time']
            sch_english_name = data['sch_english_name']
            sch_logo = data['sch_logo']
            sch_name = data['sch_name']
            sch_run_type = data['sch_run_type']
            sch_type_desc = data['sch_type_desc']
            sch_type_tag_desc = data['sch_type_tag_desc']

            item['sch_id'] = sch_id
            item['name'] = sch_name
            item['english_name'] = sch_english_name
            item['logo'] = sch_logo
            item['diploma'] = diploma_desc
            item['run_type'] = sch_run_type
            item['type'] = sch_type_desc
            if sch_type_tag_desc == "" or sch_type_tag_desc is None:
                item['tag'] = ""
            else:
                item['tag'] = ','.join(sch_type_tag_desc)
            item['grad'] = grad_desc
            item['location'] = location
            item['competent'] = sch_competent_desc
            item['create_year'] = sch_create_time
            item['province'] = province
            item['t'] = 'sch_info'
            # yield item

            # 构造详情页的请求
            detail_url = "https://www.wmzy.com/web/school?sch_id=" + sch_id
            #yield scrapy.Request(detail_url, callback=self.parse_detail_page)

            # =========构造录取招生页的请求 start=================
            # enroll_unit
            post_enroll_unit_list_data = {
                "province_id": "130000000000",
                "enroll_category": 1,
                "enroll_mode": 1,
                "sch_id": sch_id
            }
            enroll_unit_list_meta = {
                "stu_province_id": "130000000000",
                "sch_id": sch_id,
            }
            yield scrapy.Request(self.get_enroll_unit_list_url, meta=enroll_unit_list_meta,
                                 callback=self.parse_enroll_unit_list_data, method='POST', headers=self.headers,
                                 body=json.dumps(post_enroll_unit_list_data))

            # enroll_rule
            post_sch_enroll_rule_info_data = {
                "sch_id": sch_id
            }
            # yield scrapy.Request(self.get_sch_enroll_rule_info_url, callback=self.parse_sch_enroll_rule_info_data,
            #                      method='POST', headers=self.headers, body=json.dumps(post_sch_enroll_rule_info_data))
            # =========构造录取招生页的请求 end  =================

    # 解析详情页数据
    def parse_detail_page(self, response):
        """
        解析详情页的数据
        :param response:
        :return:
        """
        response_body = response.body
        result = re.findall(".*<script id=\"__NEXT_DATA__\" type=\"application/json\">(.*?)<\/script>.*", response_body)

        detail_info_item = DetailInfoItem()
        celebrity_info_item = CelebrityInfoItem()
        discipline_evaluation_item = DisciplineEvaluationItem()
        lib_evaluation_item = LibEvaluationItem()

        for x in result:
            data = json.loads(x)
            sch_detail_info = data['props']['pageProps']['schoolInfor']['sch_detail_info']
            # 师资信息
            sch_faculty_info = data['props']['pageProps']['schoolInfor']['sch_faculty_info']['sch_faculty_intro']

            sch_id = sch_detail_info['sch_id']
            sch_intro = sch_detail_info['sch_intro']
            sch_address = sch_detail_info['sch_address']
            sch_tel_num = sch_detail_info['sch_tel_num']
            sch_female_ratio = sch_detail_info['sch_female_ratio']
            sch_master_ratio = sch_detail_info['sch_master_ratio']
            sch_abroad_ratio = sch_detail_info['sch_abroad_ratio']
            sch_scholarship = sch_detail_info['sch_scholarship']
            sch_fellowship = sch_detail_info['sch_fellowship']
            canteen_desc = sch_detail_info['canteen_desc']
            stu_dorm_desc = sch_detail_info['stu_dorm_desc']

            detail_info_item['sch_faculty_info'] = sch_faculty_info
            detail_info_item['sch_id'] = sch_id
            detail_info_item['sch_intro'] = sch_intro
            detail_info_item['sch_address'] = sch_address
            detail_info_item['sch_tel_num'] = sch_tel_num
            detail_info_item['sch_female_ratio'] = sch_female_ratio
            detail_info_item['sch_master_ratio'] = sch_master_ratio
            detail_info_item['sch_abroad_ratio'] = sch_abroad_ratio
            detail_info_item['sch_scholarship'] = sch_scholarship
            detail_info_item['sch_fellowship'] = sch_fellowship
            detail_info_item['canteen_desc'] = canteen_desc
            detail_info_item['stu_dorm_desc'] = stu_dorm_desc
            detail_info_item['t'] = 'sch_detail_info'
            yield detail_info_item

            # 知名校友
            try:
                sch_celebrity_info = data['props']['pageProps']['schoolInfor']['sch_celebrity_info']
                if len(sch_celebrity_info) > 0:
                    for celebrity_info in sch_celebrity_info:
                        celebrity_info_item['sch_id'] = sch_id
                        celebrity_info_item['celebrity_name'] = celebrity_info['celebrity_name']
                        celebrity_info_item['celebrity_desc'] = celebrity_info['celebrity_desc']
                        celebrity_info_item['t'] = 'sch_celebrity_info'
                        yield celebrity_info_item
            except (IndexError, BaseException):
                print('不存在知名校友')

            # 重点学科
            try:
                discipline_evaluation_list = data['props']['pageProps']['schoolInfor']['sch_discipline_evaluation_list']['sch_discipline_evaluation_list']
                if len(discipline_evaluation_list) > 0:
                    for discipline_evaluation in discipline_evaluation_list:
                        discipline_evaluation_item['sch_id'] = sch_id
                        discipline_evaluation_item['obj_id'] = discipline_evaluation['obj_id']
                        discipline_evaluation_item['obj_name'] = discipline_evaluation['obj_name']
                        discipline_evaluation_item['obj_num'] = discipline_evaluation['obj_num']
                        discipline_evaluation_item['obj_list'] = discipline_evaluation['obj_list']
                        discipline_evaluation_item['t'] = 'discipline_evaluation'
                        yield discipline_evaluation_item
            except (IndexError, BaseException):
                print('不存在重点学科')

            # 特色培养
            try:
                sch_lib_evaluation_list = data['props']['pageProps']['schoolInfor']['sch_lib_evaluation_list']['sch_lib_evaluation_list']
                if len(sch_lib_evaluation_list) > 0:
                    for lib_evaluation in sch_lib_evaluation_list:
                        lib_evaluation_item['sch_id'] = sch_id
                        lib_evaluation_item['obj_id'] = lib_evaluation['obj_id']
                        lib_evaluation_item['obj_name'] = lib_evaluation['obj_name']
                        lib_evaluation_item['obj_num'] = lib_evaluation['obj_num']
                        lib_evaluation_item['obj_list'] = lib_evaluation['obj_list']
                        lib_evaluation_item['t'] = 'lib_evaluation'
                        time.sleep(0.001)
                        yield lib_evaluation_item
            except (IndexError, BaseException):
                print('不存在特色培养')

            # enroll_unit

    # enroll_unit_list
    def parse_enroll_unit_list_data(self, response):
        _meta = response.meta
        enroll_unit_item = EnrollUnitListItem()
        json_content = json.loads(response.body)
        if json_content['code'] == 0 and len(json_content['data']['enroll_unit_info']) > 0:
            for enroll_unit_info in json_content['data']['enroll_unit_info']:
                enroll_unit_id = enroll_unit_info['enroll_unit_id']
                enroll_unit_item['enroll_unit_code'] = enroll_unit_info['enroll_unit_code']
                enroll_unit_item['enroll_unit_id'] = enroll_unit_id
                enroll_unit_item['enroll_unit_name'] = enroll_unit_info['enroll_unit_name']
                enroll_unit_item['stu_province_id'] = _meta['stu_province_id']
                enroll_unit_item['sch_id'] = _meta['sch_id']
                enroll_unit_item['t'] = 'enroll_unit_list'
                # yield enroll_unit_item

                # sch_enroll_data
                for wenli in [1, 2]:
                    post_sch_enroll_data = {
                        "page": 1,
                        "page_size": 100,
                        "sch_id": _meta['sch_id'],
                        "enroll_unit_id": enroll_unit_id,
                        "enroll_category": 1,
                        "enroll_mode": 1,
                        "diploma_id": 1,
                        "stu_province_id": _meta['stu_province_id'],
                        "page_info": {
                            "page": 1,
                            "page_size": 10
                        },
                        "wenli": wenli,
                        "only_admission": True
                    }

                    yield scrapy.Request(self.sch_enroll_data_url, meta=_meta,
                                         callback=self.parse_sch_enroll_data, method='POST', headers=self.headers,
                                         body=json.dumps(post_sch_enroll_data))

                    # major_enroll_data
                    # 招生计划 专业录取数据
                    major_enroll_data_url = "https://www.wmzy.com/gw/api/sku/enroll_admission_service/major_enroll_data"
                    new_ncee_eu_enroll_data_url = "https://www.wmzy.com/gw/enroll_admission_service/new_ncee_eu_enroll_data"
                    for year in [2020, 2019, 2018, 2017]:
                        for diploma in [7, 5]:
                            for batch in [1, 2]:
                                # 招生计划
                                post_major_enroll_data = {
                                    "academic_year": year,
                                    "admission_year": year,
                                    "batch": batch,
                                    "batch_ex": 0,
                                    # "batch_name": "本科批",
                                    # "batch_name": "高职专科批",
                                    "diploma_id": diploma,
                                    "enroll_category": 1,
                                    "enroll_mode": 1,
                                    "enroll_stage": 0,
                                    "enroll_unit_id": enroll_unit_id,
                                    "enroll_year": year,
                                    "only_admission": False,
                                    "page": 1,
                                    "page_size": 100,
                                    "sort_key": "enroll_major_code",
                                    "sort_type": 1,
                                    "stu_province_id": _meta['stu_province_id'],
                                    "wenli": wenli,
                                    "year": year,
                                }


                                # 招生计划扩展数据
                                headers = {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
                                    'Channel': 'www.wmzy.com pc',
                                    'Content-Type': 'application/json; charset=utf-8',
                                    'Authorization': "4503446 Un8iZ/jMlpc518NfFEYMFACF4wpVApK90354kK46TSv77eh4MTr8YUJQlfe2vjGO"
                                }
                                post_major_enroll_ext_data = {
                                    "page": 1,
                                    "page_size": 100,
                                    "stu_province_id": _meta['stu_province_id'],
                                    "enroll_category": 1,
                                    "enroll_mode": 1,
                                    "enroll_stage": 0,
                                    "enroll_year": year,
                                    "sch_id": _meta['sch_id'],
                                    "enroll_unit_id": enroll_unit_id,
                                    "diploma_id": diploma,
                                    "wenli": wenli,
                                    "only_admission": False,
                                    "batch": batch,
                                    "batch_ex": 0
                                }
                                meta_major_enroll_ext_data = {
                                    "stu_province_id": _meta['stu_province_id'],
                                    "enroll_category": 1,
                                    "enroll_mode": 1,
                                    "enroll_stage": 0,
                                    "enroll_year": year,
                                    "sch_id": _meta['sch_id'],
                                    "enroll_unit_id": enroll_unit_id,
                                    "diploma_id": diploma,
                                    "wenli": wenli,
                                    "only_admission": False,
                                    "batch": batch,
                                    "batch_ex": 0,
                                    "stu_province_id": _meta['stu_province_id']
                                }

                                # 招生计划&专业录取数据
                                yield scrapy.Request(major_enroll_data_url, meta=post_major_enroll_data,
                                                     callback=self.parse_major_enroll_data, method='POST',
                                                     headers=self.headers, body=json.dumps(post_major_enroll_data))
                                # 招生计划扩展信息
                                yield scrapy.Request(new_ncee_eu_enroll_data_url, meta=meta_major_enroll_ext_data,
                                                     callback=self.parse_major_enroll_ext_data, method='POST',
                                                     headers=headers, body=json.dumps(post_major_enroll_ext_data))
    # enroll_rule_info
    def parse_sch_enroll_rule_info_data(self, response):
        enroll_rule_info_item = EnrollRuleInfoItem()
        json_content = json.loads(response.body)
        if json_content['code'] == 0:
            sch_enroll_rule_info = json_content['data']['sch_enroll_rule_info']
            enroll_rule_info_item['sch_id'] = sch_enroll_rule_info['sch_id']
            enroll_rule_info_item['academic_year'] = sch_enroll_rule_info['academic_year']
            enroll_rule_info_item['enroll_rule_title'] = sch_enroll_rule_info['enroll_rule_title']
            enroll_rule_info_item['content'] = sch_enroll_rule_info['content']
            enroll_rule_info_item['t'] = 'sch_enroll_rule_info'
            yield enroll_rule_info_item

    # parse_sch_enroll_data
    def parse_sch_enroll_data(self, response):
        _meta = response.meta
        # 补sch_detail数据
        sch_info_ext_item = SchInfoExtItem()
        sch_enroll_data_item = SchEnrollDataItem()
        json_content = json.loads(response.body)
        if json_content['code'] == 0 and 'eu_list' in json_content['data'] and len(json_content['data']['eu_list']) > 0:
            for eu_list in json_content['data']['eu_list']:
                sch_info_ext_item['province_id'] = eu_list['province_id']
                sch_info_ext_item['latest_admission_year'] = eu_list['latest_admission_year']
                sch_info_ext_item['latest_enroll_year'] = eu_list['latest_enroll_year']
                sch_info_ext_item['city_id'] = eu_list['city_id']
                sch_info_ext_item['city_id_desc'] = eu_list['city_id_desc']
                sch_info_ext_item['region_id'] = eu_list['region_id']
                sch_info_ext_item['regioin_id_desc'] = eu_list['regioin_id_desc']
                sch_info_ext_item['sch_code'] = eu_list['sch_code']
                sch_info_ext_item['nation_id'] = eu_list['nation_id']
                sch_info_ext_item['sch_id'] = eu_list['sch_id']
                sch_info_ext_item['t'] = 'sch_info_ext'
                yield sch_info_ext_item

                if "enroll_info_list" in eu_list and len(eu_list['enroll_info_list']) > 0:
                    for enroll_info in eu_list['enroll_info_list']:
                        sch_enroll_data_item['sch_id'] = eu_list['sch_id']
                        sch_enroll_data_item['enroll_unit_id'] = eu_list['enroll_unit_id']
                        sch_enroll_data_item['stu_province_id'] = _meta['stu_province_id']
                        sch_enroll_data_item['wenli'] = enroll_info['wenli']
                        sch_enroll_data_item['diploma_id'] = enroll_info['diploma_id']
                        sch_enroll_data_item['academic_year'] = enroll_info['academic_year']
                        sch_enroll_data_item['admission_count'] = enroll_info['admission_count']
                        sch_enroll_data_item['admission_ratio'] = enroll_info['admission_ratio']
                        sch_enroll_data_item['avg_score'] = enroll_info['avg_score']
                        sch_enroll_data_item['avg_score_diff'] = enroll_info['avg_score_diff']
                        sch_enroll_data_item['avg_score_equal'] = enroll_info['avg_score_equal']
                        sch_enroll_data_item['avg_score_rank'] = enroll_info['avg_score_rank']
                        sch_enroll_data_item['bao_lower_boundary_rank'] = enroll_info['bao_lower_boundary_rank']
                        sch_enroll_data_item['batch'] = enroll_info['batch']
                        sch_enroll_data_item['batch_ex'] = enroll_info['batch_ex']
                        sch_enroll_data_item['batch_name'] = enroll_info['batch_name']
                        sch_enroll_data_item['chong_lower_boundary_rank'] = enroll_info['chong_lower_boundary_rank']
                        sch_enroll_data_item['course_level_order'] = enroll_info['course_level_order']
                        sch_enroll_data_item['cwbn_type'] = enroll_info['cwbn_type']

                        # sch_enroll_data_item['enroll_category'] = enroll_info['enroll_category']
                        # sch_enroll_data_item['enroll_mode'] = enroll_info['enroll_mode']
                        # sch_enroll_data_item['enroll_plan_count'] = enroll_info['enroll_plan_count']
                        # sch_enroll_data_item['enroll_unit_code'] = enroll_info['enroll_unit_code']
                        # sch_enroll_data_item['enroll_unit_name'] = enroll_info['enroll_unit_name']

                        sch_enroll_data_item['fluctuation'] = enroll_info['fluctuation']
                        sch_enroll_data_item['match_select_course_all'] = enroll_info['match_select_course_all']
                        sch_enroll_data_item['max_score'] = enroll_info['max_score']
                        sch_enroll_data_item['max_score_diff'] = enroll_info['max_score_diff']
                        sch_enroll_data_item['max_score_equal'] = enroll_info['max_score_equal']
                        sch_enroll_data_item['max_score_rank'] = enroll_info['max_score_rank']
                        sch_enroll_data_item['min_score'] = enroll_info['min_score']
                        sch_enroll_data_item['min_score_diff'] = enroll_info['min_score_diff']
                        sch_enroll_data_item['min_score_equal'] = enroll_info['min_score_equal']
                        sch_enroll_data_item['min_score_rank'] = enroll_info['min_score_rank']
                        sch_enroll_data_item['optional_course_desc'] = enroll_info['optional_course_desc']
                        sch_enroll_data_item['predict_rank'] = enroll_info['predict_rank']
                        sch_enroll_data_item['required_course_desc'] = enroll_info['required_course_desc']
                        sch_enroll_data_item['sch_teach_location'] = enroll_info['sch_teach_location']
                        sch_enroll_data_item['special_policy'] = enroll_info['special_policy']
                        sch_enroll_data_item['special_policy_tags'] = enroll_info['special_policy_tags']
                        sch_enroll_data_item['special_policy_tags_desc'] = enroll_info['special_policy_tags_desc']
                        sch_enroll_data_item['wen_lower_boundary_rank'] = enroll_info['wen_lower_boundary_rank']
                        sch_enroll_data_item['t'] = 'sch_enroll_data'
                        yield sch_enroll_data_item

    # major_enroll_data
    def parse_major_enroll_data(self, response):
        _meta = response.meta
        # 补sch_detail数据
        major_enroll_data_item = MajorEnrollDataItem()
        json_content = json.loads(response.body)

        if json_content['code'] == 0 and 'enroll_info_list' in json_content['data'] and \
                json_content['data']['enroll_info_list'] != None and \
                len(json_content['data']['enroll_info_list']) > 0:
            for enroll_info_list in json_content['data']['enroll_info_list']:
                major_enroll_data_item['stu_province_id'] = _meta['stu_province_id']
                major_enroll_data_item['wenli'] = _meta['wenli']
                major_enroll_data_item['enroll_year'] = _meta['enroll_year']
                major_enroll_data_item['enroll_unit_id'] = _meta['enroll_unit_id']
                major_enroll_data_item['batch'] = _meta['batch']
                major_enroll_data_item['diploma_id'] = _meta['diploma_id']
                major_enroll_data_item['year'] = _meta['year']
                major_enroll_data_item['major_id'] = enroll_info_list['major_id']
                major_enroll_data_item['enroll_major_code'] = enroll_info_list['enroll_major_code']
                major_enroll_data_item['enroll_major_id'] = enroll_info_list['enroll_major_id']
                major_enroll_data_item['academic_year'] = _meta['academic_year']
                major_enroll_data_item['admission_year'] = _meta['admission_year']
                major_enroll_data_item['batch_ex'] = _meta['batch_ex']
                major_enroll_data_item['enroll_category'] = _meta['enroll_category']
                major_enroll_data_item['enroll_mode'] = _meta['enroll_mode']
                major_enroll_data_item['enroll_stage'] = _meta['enroll_stage']
                major_enroll_data_item['academic_rule'] = enroll_info_list['academic_rule']
                major_enroll_data_item['admission_count'] = enroll_info_list['admission_count']
                major_enroll_data_item['avg_score'] = enroll_info_list['avg_score']
                major_enroll_data_item['avg_score_diff'] = enroll_info_list['avg_score_diff']
                major_enroll_data_item['avg_score_rank'] = enroll_info_list['avg_score_rank']
                major_enroll_data_item['enroll_major_name'] = enroll_info_list['enroll_major_name']
                major_enroll_data_item['enroll_plan_count'] = enroll_info_list['enroll_plan_count']
                major_enroll_data_item['max_score'] = enroll_info_list['max_score']
                major_enroll_data_item['max_score_diff'] = enroll_info_list['max_score_diff']
                major_enroll_data_item['max_score_rank'] = enroll_info_list['max_score_rank']
                major_enroll_data_item['min_score'] = enroll_info_list['min_score']
                major_enroll_data_item['min_score_diff'] = enroll_info_list['min_score_diff']
                major_enroll_data_item['min_score_rank'] = enroll_info_list['min_score_rank']
                major_enroll_data_item['tuition'] = enroll_info_list['tuition']
                major_enroll_data_item['t'] = 'major_enroll_data'
                yield major_enroll_data_item

    # major_enroll_ext
    def parse_major_enroll_ext_data(self, response):
        _meta = response.meta
        major_enroll_ext_data_item = MajorEnrollExtDataItem()
        json_content = json.loads(response.body)
        print("================")
        print(json_content)
        print("================")
        if json_content['code'] == 0:
            major_enroll_ext_data = json_content['data']
            if "enroll_plan_count" in major_enroll_ext_data and major_enroll_ext_data['enroll_plan_count'] != 0:
                major_enroll_ext_data_item['stu_province_id'] = _meta['stu_province_id']
                major_enroll_ext_data_item['sch_id'] = _meta['sch_id']
                major_enroll_ext_data_item['enroll_unit_id'] = _meta['enroll_unit_id']
                major_enroll_ext_data_item['diploma_id'] = _meta['diploma_id']
                major_enroll_ext_data_item['batch'] = _meta['batch']
                major_enroll_ext_data_item['wenli'] = _meta['wenli']
                major_enroll_ext_data_item['enroll_year'] = _meta['enroll_year']
                major_enroll_ext_data_item['batch_ex'] = _meta['batch_ex']
                major_enroll_ext_data_item['enroll_category'] = _meta['enroll_category']
                major_enroll_ext_data_item['enroll_mode'] = _meta['enroll_mode']
                major_enroll_ext_data_item['enroll_stage'] = _meta['enroll_stage']
                major_enroll_ext_data_item['enroll_unit_code'] = major_enroll_ext_data['enroll_unit_code']
                major_enroll_ext_data_item['enroll_plan_count'] = major_enroll_ext_data['enroll_plan_count']
                major_enroll_ext_data_item['enroll_declare'] = major_enroll_ext_data['enroll_declare']
                major_enroll_ext_data_item['optional_course_desc'] = major_enroll_ext_data['optional_course_desc']
                major_enroll_ext_data_item['optional_course_level'] = major_enroll_ext_data['optional_course_level']
                major_enroll_ext_data_item['required_course_desc'] = major_enroll_ext_data['required_course_desc']
                major_enroll_ext_data_item['required_course_level'] = major_enroll_ext_data['required_course_level']
                major_enroll_ext_data_item['t'] = 'major_enroll_ext_data'
                yield major_enroll_ext_data_item




