import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from MyScraper.items import MyscraperItem, SentenceItem


class CNNSpider(CrawlSpider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/2020/02/04/investing/china-markets-coronavirus/index.html']

    rules = (
        # # Extract links matching 'category.php' (but not matching 'subsection.php')
        # # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=r'https://edition.cnn.com/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

        content = ' '.join(response.xpath('//*[contains(@class,"zn-body__paragraph")]//text()').getall())
        content = re.sub(r'\s+', ' ', content)

        if content != "":
            sentence_list = re.split(r"([\.\?\!])\s", content)
            l1 = sentence_list[::2]
            l2 = sentence_list[1::2]
            for item1, item2 in zip(l1, l2):
                sentence = (item1 + item2).strip()
                if sentence != "" and len(sentence)>10:
                    item = MyscraperItem()
                    item['url'] = response.url
                    item['title'] = response.xpath('//h1[@class="pg-headline"]/text()').get()
                    item['content'] = sentence
                    yield item
            # return item
        else:
            return None