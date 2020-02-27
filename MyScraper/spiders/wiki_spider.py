import re
import os
import pickle
from pathlib import Path
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urllib.parse
from MyScraper.items import WikiItem, SentenceItem
import MyScraper

class WikiSpider(CrawlSpider):
    name = 'wiki'
    lang = 'ar'
    allowed_domains = [f'{lang}.wikipedia.org']

    rules = (
        Rule(LinkExtractor(allow=f'https://{lang}.wikipedia.org/wiki/'), callback='parse_item', follow=True),
    )

    valid_url_re = re.compile(rf'https://{lang}.wikipedia.org/wiki/([^\/\:]+)')

    project_result_path = Path(MyScraper.__file__).resolve().parent / 'result'
    os.makedirs(str(project_result_path), exist_ok=True)

    result_path = project_result_path / f'{name}_{lang}_result'
    os.makedirs(str(result_path), exist_ok=True)

    html_path = result_path / f'html'
    os.makedirs(str(html_path), exist_ok=True)


    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_EXPORT_ENCODING': 'utf-8',
        # 'FEED_URI': f'wiki_a.json'
        # 'DEPTH_LIMIT': 2,
    }

    
    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.start = kwargs.get('start')
        self.start_urls = [f"https://{self.lang}.wikipedia.org/wiki/{self.start}"]
        self.log(f'start url {self.start_urls}', 50)

        # self.custom_settings = {
        #     'FEED_FORMAT': 'jsonlines',
        #     'FEED_EXPORT_ENCODING': 'utf-8',
        #     'FEED_URI': str(self.result_path / f'wiki_{self.start}.json')
        #     # 'DEPTH_LIMIT': 2,
        # }

        self.pickle_path = self.result_path / f"{self.name}_{self.lang}_{self.start}.pickle"
        try:
            with open(str(self.pickle_path), "rb") as f:
                self.titles_seen = pickle.load(f)
            self.logger.info(f'load title dict from disk {self.pickle_path}')
        except Exception as e:
            self.titles_seen = set()
            self.logger.info(f'can not found title dict, start a new one')

    def closed(self, reason):

        with open(str(self.pickle_path), "wb") as f:
            pickle.dump(self.titles_seen, f)

        self.logger.info(f'save title dict to disk {self.pickle_path}')

            
    # def parse(self, response):
    def parse_item(self, response):

        # avoid bad response
        if not response.status == 200:
            return None

        m = re.match(self.valid_url_re, response.url)

        # avoid strange title page
        if not m:
            return None

        title = urllib.parse.unquote(m.group(1))

        # avoid duplicate
        if title in self.titles_seen:
            self.logger.warning(f'Duplicate page will skip')
            return None

        ################# real start
        self.logger.info('Found one page! %s', response.url)

        self.titles_seen.add(title)

        self.logger.info(f'Page title {title}')

        filename = f'wiki_{self.lang}_{title}.html'
        with open(f'{self.html_path}/{filename}', 'wb') as f:
            f.write(response.body)

        item = WikiItem()
        item['url'] = urllib.parse.unquote(response.url)
        item['title'] = title
        item['filename'] = filename

        return item


        # paragraphs = response.xpath('//div[@id="mw-content-text"]/div/p[not(@class)]').extract()
        #
        # content = ' '.join([converter.handle(paragraph) for paragraph in paragraphs])
        #
        # content = regex_process(content)
        #
        # if content != "":
        #     sentence_list = re.split(r"([\.\?\!])\s", content)
        #     l1 = sentence_list[::2]
        #     l2 = sentence_list[1::2]
        #     index = 0
        #     for item1, item2 in zip(l1, l2):
        #         sentence = (item1 + item2).strip()
        #         if sentence != "" and len(sentence)>50:
        #             item = WikiItem()
        #             item['url'] = response.url
        #             item['content'] = sentence
        #             item['index'] = index
        #             index += 1
        #             yield item
        #     # return item
        # else:
        #     return None