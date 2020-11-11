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
    # ======录取招生页请求url end  ======

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Channel': 'www.wmzy.com pc',
        'Content-Type': 'application/json; charset=utf-8'
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
            #yield scrapy.Request(self.get_enroll_unit_list_url, meta=enroll_unit_list_meta, callback=self.parse_enroll_unit_list_data,
            #                     method='POST', headers=self.headers, body=json.dumps(post_enroll_unit_list_data))

            # enroll_rule
            post_sch_enroll_rule_info_data = {
                "sch_id": sch_id
            }
            yield scrapy.Request(self.get_sch_enroll_rule_info_url, callback=self.parse_sch_enroll_rule_info_data,
                                 method='POST', headers=self.headers, body=json.dumps(post_sch_enroll_rule_info_data))
            # =========构造录取招生页的请求 end  =================

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
                enroll_unit_item['enroll_unit_code'] = enroll_unit_info['enroll_unit_code']
                enroll_unit_item['enroll_unit_id'] = enroll_unit_info['enroll_unit_id']
                enroll_unit_item['enroll_unit_name'] = enroll_unit_info['enroll_unit_name']
                enroll_unit_item['stu_province_id'] = _meta['stu_province_id']
                enroll_unit_item['sch_id'] = _meta['sch_id']
                enroll_unit_item['t'] = 'enroll_unit_list'
                yield enroll_unit_item

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

