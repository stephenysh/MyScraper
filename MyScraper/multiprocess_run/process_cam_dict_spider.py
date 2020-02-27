import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from MyScraper.spiders.cam_dict_spider import CamDictSpider

from multiprocessing import Process

from string import ascii_lowercase

parser = argparse.ArgumentParser()

args = parser.parse_args()

settings = get_project_settings()

# for single_char in ascii_lowercase:
#
#     settings.attributes['FEED_URI'].set(f'cam_dict_{single_char}.json',0)
#
#     process = CrawlerProcess(settings)
#
#     spider = CamDictSpider
#
#     dispatcher.connect(set_result, signals.item_scraped)
#
#     process.crawl(spider, char=single_char)
#
#     # process.start(stop_after_crawl=False)
# process.start()



def crawl(**kwargs):
    crawler = CrawlerProcess(settings)
    crawler.crawl(CamDictSpider, char=kwargs["char"])
    crawler.start()


process_list = []
for single_char in ascii_lowercase:

    settings.attributes['FEED_URI'].set(f'cam_dict_{single_char}.json',0)

    process = Process(target=crawl, kwargs={"char": single_char})

    # process = CrawlerProcess(settings)
    # process.crawl(CamDictSpider, char=single_char)

    process.start()
    process_list.append(process)

for process in process_list:
    process.join()
