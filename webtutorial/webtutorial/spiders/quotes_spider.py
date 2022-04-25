import scrapy
from scrapy.loader import ItemLoader
from webtutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ["http://quotes.toscrape.com"]


    def parse(self, response):

        quotes = response.css("div .quote")
        for quote in quotes:
            print("______________________________________________________________")
            print(quote)
            print("______________________________________________________________")
            loader = ItemLoader(item=QuoteItem(), selector = quote)
            loader.add_css("quote_content", ".text::text")
            loader.add_css("tags", ".tag::text")
            loader.add_css("author_name", ".author::text")
            quote_item = loader.load_item()
            
            author_links = quote.css(".author + a")
            yield from response.follow_all(author_links, self.parse_author, meta={'quote_item': quote_item}, dont_filter = True)
            

        # pagination_links = response.css('li.next a')
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):

        quote_item = response.meta["quote_item"]
        loader = ItemLoader(item=quote_item, response=response)

        loader.add_css("author_birthday", ".author-born-date::text")
        loader.add_css("author_bornlocation", ".author-born-location::text")
        loader.add_css("author_bio", ".author-description::text")
        yield loader.load_item()

