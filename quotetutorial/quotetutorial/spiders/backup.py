import scrapy
from ..items import QuotetutorialItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 1
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):

        items = QuotetutorialItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()

            items["title"] = title
            items["author"] = author
            items["tag"] = tag

            yield items

        # next_page = response.css('li.next a::attr(href)').get()
        next_page = 'https://quotes.toscrape.com/page/' + str(QuotesSpider.page_number) + '/'

        print("next_page")
        if QuotesSpider.page_number < 11:
            QuotesSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
