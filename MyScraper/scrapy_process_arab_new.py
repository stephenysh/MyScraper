import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater
from MyScraper.spiders.arab_bbc_spider import WikiSpider

parser = argparse.ArgumentParser()

parser.add_argument("--name")

parser.add_argument("--start", required=True)

parser.add_argument("--id", required=True)

args = parser.parse_args()

settings = get_project_settings()

settings.attributes['FEED_URI'].set(f'arab_new_{args.id}.json',0)
settings.attributes['FEED_FORMAT'].set('jsonlines',0)

process = CrawlerProcess(settings)

spider = WikiSpider

def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)

def crash(failure):
    print('oops, spider crashed')
    print(failure.getTraceback())

def _crawl(result, spider):
    deferred = process.crawl(spider, start=args.start, id=args.id)
    deferred.addCallback(lambda results: print('waiting 10 seconds before restart...'))
    deferred.addErrback(crash)  # <-- add errback here
    deferred.addCallback(sleep, seconds=10)
    deferred.addCallback(_crawl, spider)
    return deferred

_crawl(None, spider)
process.start()
