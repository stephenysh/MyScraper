import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

parser = argparse.ArgumentParser()

parser.add_argument("--name", required=True)

parser.add_argument("--start", required=True)

parser.add_argument("--id", required=True)

args = parser.parse_args()

process = CrawlerProcess(get_project_settings())

while True:
    process.crawl(args.name, start=args.start, id=args.id)
    process.start()

