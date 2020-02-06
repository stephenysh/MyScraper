import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from MyScraper.items import WikiItem, SentenceItem

# from scrapy.selector import HtmlXPathSelector
import html2text

converter = html2text.HTML2Text()
converter.ignore_links = True

_re_multi_space = re.compile(r"\s+")
_re_bold = re.compile(r"\*\*([^\*]+)\*\*")
_re_ital = re.compile(r"\_([^\_]+)\_")
_re_ref = re.compile(r"\[\d+\]")
_re_img = re.compile(r"\*\[\!\[[^\[]+\]\([^\(]+\)\]\:")
_re_start_bracket = re.compile(r"\*\[[^\[]+\]\:")
_re_bracket = re.compile(r"\([^\(]+\)")

def regex_process(text):
    text = re.sub(_re_multi_space, " ", text)
    text = re.sub(_re_bold, lambda match: match.group(1), text)
    text = re.sub(_re_ital, lambda match: match.group(1), text)
    text = re.sub(_re_ref, "", text)
    text = re.sub(_re_img, "", text) # img should before start bracket
    text = re.sub(_re_start_bracket, "", text)
    text = re.sub(_re_bracket, "", text)
    return text

class WikiSpider(CrawlSpider):
    name = 'arab_bbc'
    allowed_domains = ['www.bbc.com']

    rules = (
        Rule(LinkExtractor(allow=['https://www.bbc.com/arabic/']), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        # self.start_urls = [f"https://en.wikipedia.org/wiki/{kwargs.get('start')}"]
        self.start_urls = [f"https://www.bbc.com/arabic/world-51312319"]



    def parse(self, response):
    # def parse_item(self, response):

        self.logger.info('Hi, this is an item page! %s', response.url)

        paragraphs = response.xpath('//div[@class="story-body__inner"]//p').extract()

        contents = [converter.handle(paragraph) for paragraph in paragraphs]

        index = 0

        for content in contents:
            content = regex_process(content)
            content = ' '.join(content.split('\n'))

            if content != "":

                sentence_list = re.split(r"([\.\?\!])", content)
                # sentence_list = [content]

                if len(sentence_list) == 1:
                    item = WikiItem()
                    item['url'] = response.url
                    item['content'] = sentence_list[0]
                    item['index'] = index
                    index += 1
                    yield item

                l1 = sentence_list[::2]
                l2 = sentence_list[1::2]

                # print(sentence_list)

                for item1, item2 in zip(l1, l2):
                    sentence = (item1 + item2).strip()
                    if sentence != "" and len(sentence)>50:
                        item = WikiItem()
                        item['url'] = response.url
                        item['content'] = sentence
                        item['index'] = index
                        index += 1
                        yield item
                # return item
            else:
                yield None