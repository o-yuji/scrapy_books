import scrapy


class BooksBasicSpider(scrapy.Spider):
    name = "books_basic"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"]

    def parse(self, response):
        books = response.xpath('//h3')

        for book in books:
            yield response.follow(url=book.xpath('./a/@href').get(),callback=self.parse_item)

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page[0],callback=self.parse)
    
    def parse_item(self,response):
        title = response.xpath('//div[contains(@class,"product_main")]/h1/text()').get()
        price = response.xpath('//p[@class="price_color"]/text()').get()
        stock = response.xpath('//div[contains(@class,"product_main")]/p[@class="instock availability"]/text()').getall()
        rating = response.xpath('//div[contains(@class,"product_main")]/p[contains(@class,"star-rating")]/@class').get()
        upc = response.xpath('//tbody/tr/th[contains(text(),"UPC")]/following-sibling::td[1]/text()').get()
        numberOfReviews = response.xpath('//th[contains(text(),"Number of reviews")]/following-sibling::td/text()').get()

        yield{
            'title':title,
            'price':price,
            'stock':stock,
            'rating':rating,
            'upc':upc,
            'numberOfReviews':numberOfReviews,
        }