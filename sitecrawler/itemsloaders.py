from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

# Okay orignally this took a relative link and made it absolute by appending it to base url
# e.g., (lambda x: domain + x) but because my duplicate pipeline does this, this code was duplicating the base URL.
# It does not do anything anymore. Not sure what to do!
class SitecrawlerItemLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    url_in = MapCompose(lambda x: x)
