import re
import random
import pickle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from MyScraper.items import CamDictItem
from MyScraper.regex_util import regex_process
from MyScraper.html2text_util import converter


class CamDictSpider(CrawlSpider):
    name = 'cam_dict'
    allowed_domains = ['dictionary.cambridge.org']

    rules = (
        Rule(LinkExtractor(allow=[r'https://dictionary.cambridge.org/dictionary/english-arabic/',
                                  'https://dictionary.cambridge.org/browse/english-arabic/']), callback='parse_item', follow=True),
    )

    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        'FEED_FORMAT': 'jsonlines',
        # 'FEED_URI': f'cam_dict_.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEPTH_LIMIT': 2,
    }

    def __init__(self, *args, **kwargs):
        super(CamDictSpider, self).__init__(*args, **kwargs)

        self.id = kwargs.get('char')

        self.start_urls = [f'https://dictionary.cambridge.org/browse/english-arabic/{self.char}/']


    # def parse(self, response):
    def parse_item(self, response):

        if not re.match(r'https://dictionary\.cambridge\.org/dictionary/english-arabic/' + self.char + r'[0-9a-zA-Z]{1,}/?', response.url):
            return None # must use return, will not run the below

        item = CamDictItem()
        item['url'] = response.url
        item['en_wd'] = response.xpath('//span[@class="hw dhw"]//text()').get().strip()
        item['ar_wd'] = response.xpath('//span[@class="trans dtrans dtrans-se "]//text()').get().strip()
        yield item