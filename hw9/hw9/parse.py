import scrapy
from scrapy.crawler import CrawlerProcess
import unicodedata


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json", 'LOG_ENABLED': 'False'}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            fullname = quote.xpath("span/small/text()").get()
            author_link = quote.xpath(".//span/a/@href").get()
            if author_link:
                yield response.follow(author_link, callback=self.parse_author, meta={'fullname': fullname})
        
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_author(self, response):
        fullname = response.meta['fullname']
        # fullname = response.xpath("//h3[@class='author-title']/text()").get()
        born_date = response.xpath("//span[@class='author-born-date']/text()").get()
        born_location = response.xpath("//span[@class='author-born-location']/text()").get()
        description = response.xpath("//div[@class='author-description']/text()").get()
        description = ''.join(description).strip().replace('\n', '')
        yield {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "qoutes.json", 'LOG_ENABLED': 'False'}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get()
            quote_text = quote.xpath("span[@class='text']/text()").get()
            yield{
                "tags": tags,
                "author": author,
                "quote": quote_text
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


process = CrawlerProcess()
process.crawl(AuthorsSpider)
process.crawl(QuotesSpider)
process.start()