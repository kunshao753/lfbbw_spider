# coding=utf-8
import scrapy
from scrapy.http import Request
from spiderMan.items import SpiderManItem
from spiderMan.items import DetailInfoItem
import sys
import json
import re
reload(sys)
sys.setdefaultencoding('utf-8')


class WmzySchInfoSpider(scrapy.Spider):
    name = 'wmzy_sch_info'
    allowed_domains = ['wmzy.com']
    start_url = 'https://www.wmzy.com/gw/api/sku/sku_service/sch_complete'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Channel': 'www.wmzy.com pc',
        'Content-Type': 'application/json; charset=utf-8'
    }

    type_desc = {
        "综合": 1,
        "工科": 2,
        "农业": 3,
        "林业": 4,
        "医药": 5,
        "师范": 6,
        "语言": 7,
        "财经": 8,
        "政法": 9,
        "体育": 10,
        "艺术": 11,
        "民族": 12,
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
            # sch_run_type_desc = data['sch_run_type_desc']
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
            yield item

            # 构造详情页的请求
            detail_url = "https://www.wmzy.com/web/school?sch_id=" + sch_id
            yield scrapy.Request(detail_url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        """
        解析详情页的数据
        :param response:
        :return:
        """
        response_body = response.body
        result = re.findall(".*<script id=\"__NEXT_DATA__\" type=\"application/json\">(.*?)<\/script>.*", response_body)

        detail_info_item = DetailInfoItem()

        for x in result:
            data = json.loads(x)
            sch_detail_info = data['props']['pageProps']['schoolInfor']['sch_detail_info']
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