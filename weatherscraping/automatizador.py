import schedule
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app import enviar_email
from time import sleep
from weatherscraping.spiders.weatherspider import WeatherspiderSpider


def run_spider():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(WeatherspiderSpider)
    process.start()


schedule.every(1).minutes.do(run_spider)

while True:
    schedule.run_pending()
    sleep(1)
