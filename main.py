import os
import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess

from create_read_write.filling_db import main


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuoteItem(Item):
    tags = Field()
    author = Field()
    text = Field()


class QuotesPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        if 'text' in adapter.keys():
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        if not os.path.exists("data"):
            os.makedirs("data")
        with open("data/quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        with open("data/author.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)


class QuotesSpider(scrapy.Spider):
    name = "to_scrapy"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {
        QuotesPipline: 100,
    }}

    def parse(self, response, **kwargs):
        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small[@class='author']/text()").get().strip()
            text = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(text=text, author=author, tags=tags)
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.parse_author)
        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response, **kwargs):  # noqa
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath('h3[@class="author-title"]/text()').get().strip()
        born_date = content.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        born_location = content.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        description = content.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    main()
