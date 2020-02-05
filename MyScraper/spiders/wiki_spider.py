import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from MyScraper.items import MyscraperItem, SentenceItem

# from scrapy.selector import HtmlXPathSelector
import html2text

converter = html2text.HTML2Text()
converter.ignore_links = True

_re_multi_space = re.compile(r"\s+")
_re_bold = re.compile(r"\*\*([^\*]+)\*\*")
_re_ital = re.compile(r"\_([^\_]+)\_")
_re_ref = re.compile("\[\d+\]")

def regex_process(text):
    text = re.sub(_re_multi_space, " ", text)
    text = re.sub(_re_bold, lambda match: match.group(1), text)
    text = re.sub(_re_ital, lambda match: match.group(1), text)
    text = re.sub(_re_ref, "", text)
    return text

class WikiSpider(CrawlSpider):
    name = 'wiki'
    allowed_domains = ['en.wikipedia.org']

    rules = (
        Rule(LinkExtractor(allow='https://en.wikipedia.org/wiki/'), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://en.wikipedia.org/wiki/{kwargs.get('start')}"]


    def parse(self, response):
    # def parse_item(self, response):

        self.logger.info('Hi, this is an item page! %s', response.url)

        paragraphs = response.xpath('//div[@id="mw-content-text"]/div/p[not(@class)]').extract()

        content = ' '.join([converter.handle(paragraph) for paragraph in paragraphs])

        content = regex_process(content)

        if content != "":
            sentence_list = re.split(r"([\.\?\!])\s", content)
            l1 = sentence_list[::2]
            l2 = sentence_list[1::2]
            index = 0
            for item1, item2 in zip(l1, l2):
                sentence = (item1 + item2).strip()
                if sentence != "" and len(sentence)>50:
                    item = MyscraperItem()
                    item['url'] = response.url
                    item['title'] = response.xpath('//h1[@id="firstHeading"]/text()').get()
                    item['content'] = sentence
                    item['index'] = index
                    index += 1
                    yield item
            # return item
        else:
            return None