# coding=utf-8
import scrapy
from scrapy.http import Request
from spiderMan.items import ProvinceRegisterConfigItem
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')


class WmzyProvinceInfoSpider(scrapy.Spider):
    name = 'wmzy_province_info'
    allowed_domains = ['wmzy.com']
    get_province_register_config_url = "https://www.wmzy.com/gw/user_service/get_province_register_config?enroll_category=1&province_id="

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Channel': 'www.wmzy.com pc',
        'Content-Type': 'application/json; charset=utf-8',
    }

    # 需要重写start_requests()方法。
    def start_requests(self):
        province_ids = {
            "650000000000", "640000000000", "630000000000", "620000000000", "610000000000", "530000000000",
        "520000000000",
            "510000000000", "500000000000", "460000000000", "450000000000", "440000000000", "430000000000",
        "420000000000",
            "410000000000", "370000000000", "360000000000", "350000000000", "340000000000", "330000000000",
        "320000000000",
            "310000000000", "230000000000", "220000000000", "210000000000", "150000000000", "140000000000",
        "130000000000","120000000000", "110000000000"
        }

        for province_id in province_ids:
            url = self.get_province_register_config_url + province_id
            meta = {
                'province_id': province_id,
                'enroll_category': 1
            }
            request = Request(url, meta=meta, callback=self.parse, method='GET', headers=self.headers)

            yield request

    def parse(self, response):
        json_content = json.loads(response.body)

        item = ProvinceRegisterConfigItem()
        _meta = response.meta
        if json_content['code'] == 0:
            data = json_content['data']
            print(data)
            item['province_id'] = _meta['province_id']
            item['enroll_category'] = _meta['enroll_category']
            item['bk_max_score'] = data['bk_max_score']
            item['bk_rank_type'] = data['bk_rank_type']
            item['course_info'] = "" if data['course_info'] is None else json.dumps(data['course_info'])
            item['course_level_info'] = "" if data['course_level_info'] is None else json.dumps(data['course_level_info'])
            item['diploma_type'] = data['diploma_type']
            item['max_score'] = data['max_score']
            item['need_course'] = 1 if data['need_course'] is True else 0
            item['need_course_level'] = 1 if data['need_course_level'] is True else 0
            item['need_diploma'] = 1 if data['need_diploma'] is True else 0
            item['need_wenli'] = 1 if data['need_wenli'] is True else 0
            item['province_score_has_publish'] = 1 if data['province_score_has_publish'] is True else 0
            item['rank_type'] = data['rank_type']
            item['ysw_max_score'] = data['ysw_max_score']
            item['zk_max_score'] = data['zk_max_score']
            item['zk_rank_type'] = data['zk_rank_type']
            item['t'] = 'province_register_config'
            yield item




