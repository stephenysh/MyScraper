import os
import sys
import argparse
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
sys.path.append(str(Path(__file__).resolve().parent / '..' / '..'))
print(sys.path[-1])
from MyScraper.spiders.wiki_spider import WikiSpider
from multiprocessing import Process

from string import ascii_lowercase

parser = argparse.ArgumentParser()

args = parser.parse_args()

settings = get_project_settings()



def crawl(**kwargs):
    crawler = CrawlerProcess(settings)
    crawler.crawl(WikiSpider, start=kwargs["start"])
    crawler.start()


process_list = []
for single_char in ['ويكي']:
# for single_char in ['zack']:
    # process = Process(target=crawl, kwargs={"start": single_char})

    # process.start()
    # process_list.append(process)

    json_file = str(WikiSpider.result_path / f'{WikiSpider.name}_{WikiSpider.lang}_{single_char}.json')
    settings.attributes['FEED_URI'].set(json_file, 0)

    crawler = CrawlerProcess(settings)
    crawler.crawl(WikiSpider, start=single_char)
    crawler.start()


