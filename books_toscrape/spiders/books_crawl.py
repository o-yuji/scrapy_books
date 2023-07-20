import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging

class BooksCrawlSpider(CrawlSpider):
    name = "books_crawl"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3/a"), 
             callback="parse_item", follow=False),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"),
             follow=True)
        )

    def get_stock(self,stock):
        if stock:
            return stock[1].replace('\n','').strip()

    def parse_item(self, response):
        logging.info(response.url)
        yield {
            'title': response.xpath("//h1/text()").get(),
            'price': response.xpath("//div[contains(@class,'product_main')]/p[@class='price_color']/text()").get(),
            'stock': self.get_stock(response.xpath('//div[contains(@class,"product_main")]/p[contains(@class,"instock")]/text()').getall()),
            'rating': response.xpath('//div[contains(@class,"product_main")]/p[contains(@class,"star-rating")]/@class').get(),
            'UPC': response.xpath('//tbody/tr[1]/td/text()').get(),
            'review': response.xpath('//tbody//th[contains(text(),"Number of reviews")]/following-sibling::td/text()').get()
        }