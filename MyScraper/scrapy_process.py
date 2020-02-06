import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy.settings

parser = argparse.ArgumentParser()

parser.add_argument("--name", required=True)

parser.add_argument("--start", required=True)

parser.add_argument("--id", required=True)

args = parser.parse_args()

settings = get_project_settings()

settings.attributes['FEED_URI'].set(f'{args.name}_{args.id}.json',0)
settings.attributes['FEED_FORMAT'].set('jsonlines',0)


while True:
    process = CrawlerProcess(settings)
    process.crawl(args.name, start=args.start, id=args.id)
    process.start()

