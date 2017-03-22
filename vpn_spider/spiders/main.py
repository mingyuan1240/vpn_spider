import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from vpn_spider.items import Server

class BaseSpider(scrapy.Spider):
    def __init__(self):
        self.link_extractor = LxmlLinkExtractor(allow=self.allow_urls)

    def parse(self, response):
        for proxy in response.xpath(self.item_xpath):
            server = Server()
            for k, xpath in self.attr_xpath_map.items():
                if k in server.fields:
                    v = proxy.xpath(xpath).extract_first()
                    if v: v = v.strip()
                    server[k] = v
            yield server
            
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(response.urljoin(link.url), callback=self.parse)

class Proxy360Spider(BaseSpider):
    name = "proxy360"
    allowed_domains = ["proxy360.cn"]
    start_urls = ['http://www.proxy360.cn/default.aspx']
    allow_urls = (r'www\.proxy360\.cn/Region/\w+')
    item_xpath = '//div[@class="proxylistitem"]'
    attr_xpath_map = {
        'host': 'div/span[1]/text()',
        'port': 'div/span[2]/text()',
        'anonymous_type': 'div/span[3]/text()',
        'region': 'div/span[4]/text()'
        }

class XiciSpider(BaseSpider):
    name = 'xici'
    allowed_domains = ["xicidaili.com"]
    start_urls = ['http://www.xicidaili.com/nn/', 'http://www.xicidaili.com/nt/', 'http://www.xicidaili.com/wn/', 'http://www.xicidaili.com/wt/']
    allow_urls = (r'/nn/\d+', r'/nt/\d+', r'/wn/\d+', r'/wn/\d+')
    item_xpath = '//table[@id="ip_list"]/tr[@class!="subtitle"]'
    attr_xpath_map = {
        'host': 'td[2]/text()',
        'port': 'td[3]/text()',
        'region': 'td[4]/text()',
        'anonymous_type': 'td[5]/text()',
        'type': 'td[6]/text()'
        }

class KuaidailiSpider(BaseSpider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['http://www.kuaidaili.com/free/inha/', 'http://www.kuaidaili.com/free/outha/']
    allow_urls = (r'/free/inha/\d+/$', r'/free/outha/\d+/$')
    item_xpath = '//div[@id="list"]//tbody/tr'
    attr_xpath_map = {
        'host': 'td[1]/text()',
        'port': 'td[2]/text()',
        'anonymous_type': 'td[3]/text()',
        'type': 'td[4]/text()',
        'region': 'td[5]/text()'
        }
