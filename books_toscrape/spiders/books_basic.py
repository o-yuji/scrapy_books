import scrapy


class BooksBasicSpider(scrapy.Spider):
    name = "books_basic"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"]

    def parse(self, response):
        article = response.xpath('//article[@class="product_pod"]')
        books = article.xpath('.//h3/a/text()').getall()
        prices = article.xpath('.//div[@class="product_price"]/p[1]/text()').getall()
        urls = article.xpath('.//h3/a/@href').getall()

        for book,price,url in zip(books,prices,urls):
            yield{
                'book':book,
                'price':price,
                'url':url
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page[0],callback=self.parse)