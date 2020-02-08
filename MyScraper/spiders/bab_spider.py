import re
import random
import pickle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from MyScraper.items import BabItem
from MyScraper.regex_util import regex_process
from MyScraper.html2text_util import converter


def regex_process(text):
    text = text.replace('\n', '')

    text = re.sub(r'<span.*?>.*</span>', '', text)

    text = re.sub('<.*?>', '', text)

    return text

class BabSpider(CrawlSpider):
    name = 'bab'
    allowed_domains = ['en.bab.la']

    rules = (
        Rule(LinkExtractor(allow=[r'https://en.bab.la/dictionary/english-arabic/']), callback='parse_item', follow=True),
    )

    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        'FEED_FORMAT': 'jsonlines',
        # 'FEED_URI': f'cam_dict_.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEPTH_LIMIT': 2,
    }

    def __init__(self, *args, **kwargs):
        super(BabSpider, self).__init__(*args, **kwargs)

        self.id = kwargs.get('char')

        self.start_urls = [f'https://en.bab.la/dictionary/english-arabic/{self.char}/']
        # self.start_urls = [f'https://en.bab.la/dictionary/english-arabic/awake']



    def parse_item(self, response):

        url = response.url.replace(f'https://en.bab.la/dictionary/english-arabic/', '')

        if not re.match(self.char + r'[0-9a-zA-Z\-]{1,}', url):
            return None # must use return, will not run the below

        for section in response.xpath('//span[@class="section-label"]'):
            if section.xpath('text()').get() == 'Context sentences':

                contents = section.xpath('//div[@class="dict-example"]')
                for index, content in enumerate(contents):

                    en_str = content.xpath('div[@class="dict-source"]').get()
                    ar_str = content.xpath('div[@class="dict-result"]').get()

                    en_str = regex_process(en_str)
                    ar_str = regex_process(ar_str)

                    if '' in [en_str, ar_str]:
                        continue

                    item = BabItem()
                    item['url'] = response.url
                    item['en_str'] = en_str
                    item['ar_str'] = ar_str
                    item['idx'] = index

                    yield item