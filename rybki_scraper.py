import scrapy

class RybkaSpider(scrapy.Spider):
    name = 'pajak_wodny'

    def start_requests(self):
        urls = ['https://rybyakwariowe.eu/gatunki-ryb-akwariowych/']
        for i in range(2, 19):
            urls.append("https://rybyakwariowe.eu/gatunki-ryb-akwariowych/page/" + str(i) + "/")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_general)


    def parse_general(self, response):
        for rybka in response.css('article'):
            yield {
                'link_to_details': rybka.xpath('header/h2[@class="single-title"]/a/@href').get(),
                'name': rybka.css('h2.single-title>a.u-url::text').get(),
                'latin_name': rybka.css('h3.single-subtitle::text').get(),
                'temperature': rybka.xpath('ul[@class="desc-fish wrap-box"]/li[@class="desc-fish__ico desc-fish__ico--temp"]/text()').get(),
                'length': rybka.xpath('ul[@class="desc-fish wrap-box"]/li[@class="desc-fish__ico desc-fish__ico--size"]/text()').get(),
                'location': rybka.xpath('ul[@class="desc-fish wrap-box"]/li[@class="desc-fish__ico desc-fish__ico--biotop"]/a/text()').get(),
            }

'''
    def parse_general(self, response):
        try:
            print(response)
        except:
            print("An exception occurred")

        for rybka in response.css('article'):
            links = str(rybka.css('header/h2[@class="single-title"]/a/@href').get())

        for link in links:
            yield response.follow(url= link, callback= self.parse_single_rybka) 


    def parse_single_rybka(self, response):

        for rybka in response.css('article'):
            yield {
                'name': rybka.xpath('@id').get()#/header/h1[@class="entry-title single-title"]/a/text()').get()
            #'latin_name':
            #'temperature':
            #'length':
            #'location':
            #'food':
            #'kryjowka_info':
            #'breeding_type':
            }'''