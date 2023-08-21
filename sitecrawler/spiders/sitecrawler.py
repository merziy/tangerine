# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from sitecrawler.itemsloaders import SitecrawlerItemLoader
from sitecrawler.items import SitecrawlerItem
from urllib.parse import urlparse, urljoin

class SiteCrawler(scrapy.Spider):
    name = 'sitecrawler'

    def __init__(self, domain=None):
        super(SiteCrawler, self).__init__()
        if domain:
            self.allowed_domains = [domain]
            self.start_urls = [f"https://www.{domain}/"]
        else:
            self.allowed_domains = ['juicyorange.com']
            self.start_urls = [f"https://www.juicyorange.com/"]
        self.found_urls = set()

    def parse(self, response):
        anchor_links = response.xpath('//a')

        for anchor in anchor_links:
            loader = SitecrawlerItemLoader(item=SitecrawlerItem(), selector=anchor)
            relative_url = anchor.xpath('@href').get()
    
            if relative_url:
                parsed_url = urlparse(relative_url)
                if not parsed_url.scheme or not parsed_url.netloc:
                    absolute_url = urljoin(response.url, relative_url)

            if self.allowed_domains[0] in absolute_url:
                loader.add_value('url', absolute_url)
                yield loader.load_item()

                self.found_urls.add(absolute_url)

        next_page = response.xpath('//a[@rel="next"]/@href').get()

        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            if self.allowed_domains[0] in next_page_url:
                yield scrapy.Request(next_page_url, callback=self.parse)

    def closed(self, reason):
        print("Found URLs:")
        for url in self.found_urls:
            print(url)
