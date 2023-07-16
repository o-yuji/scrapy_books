import scrapy


class BooksBasicSpider(scrapy.Spider):
    name = "books_basic"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"]

    def parse(self, response):
        books = response.xpath('//h3')

        for book in books:
            # yield{
            #     'title':book.xpath('.//a/@title').get(),
            #     'url':url,
            #     'price':price,
            # }
            yield response.follow(url=book.xpath('./a/@href').get(),callback=self.parse_item)


        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page[0],callback=self.parse)
    
    def parse_item(self,response):
        title = response.xpath('//div[contains(@class,"product_main")]/h1/text()').get()
        price = response.xpath('//p[@class="price_color"]/text()').get()
        
        yield{
            'title':title,
            'price':price,
        }