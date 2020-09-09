import scrapy


class WmzySchInfoSpider(scrapy.Spider):
    name = 'wmzy_sch_info'
    allowed_domains = ['wmzy.com']
    start_urls = ['http://https://www.wmzy.com/gw/api/sku/sku_service/sch_complete/']

    def parse(self, response):
        pass
