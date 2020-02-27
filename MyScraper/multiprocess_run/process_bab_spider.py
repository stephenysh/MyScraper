import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from MyScraper.spiders.bab_spider import BabSpider

from multiprocessing import Process

from string import ascii_lowercase

parser = argparse.ArgumentParser()

args = parser.parse_args()

settings = get_project_settings()



def crawl(**kwargs):
    crawler = CrawlerProcess(settings)
    crawler.crawl(BabSpider, char=kwargs["char"])
    crawler.start()


process_list = []
for single_char in ascii_lowercase:

    settings.attributes['FEED_URI'].set(f'bab_{single_char}.json', 0)

    process = Process(target=crawl, kwargs={"char": single_char})

    # process = CrawlerProcess(settings)
    # process.crawl(BabSpider, char=single_char)

    process.start()
    process_list.append(process)

for process in process_list:
    process.join()
