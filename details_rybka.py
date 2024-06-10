import scrapy
import pandas as pd

class SingleRybkaSpider(scrapy.Spider):
    name = 'single_rybka'

    def start_requests(self):
        df = pd.read_csv('rybki.csv')
        links = df["link_to_details"]

        urls = []
        for link in links:
            urls.append("https://rybyakwariowe.eu" + str(link))

        for url in urls:
            yield scrapy.Request(url= url, callback=self.parse_general)


    def parse_general(self, response):
        '''for rybka in response
            yield {
                'link_to_details': response.xpath('header/h2[@class="single-title"]/a/@href').get(),
                'name': rybka.css('h2.single-title>a.u-url::text').get(),
                'latin_name': rybka.css('h3.single-subtitle::text').get(),
                'temperature': rybka.xpath('ul[@class="desc-fish wrap-box"]/li[@class="desc-fish__ico desc-fish__ico--temp"]/text()').get(),
                'length': rybka.xpath('ul[@class="desc-fish wrap-box"]/li[@class="desc-fish__ico desc-fish__ico--size"]/text()').get(),
                'location': rybka.xpath('ul[@class="desc-fish wrap-box"]/li[@class="desc-fish__ico desc-fish__ico--biotop"]/a/text()').get(),
            }'''
