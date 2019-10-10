import scrapy
from urllib.parse import urljoin
from jobparser.items import XxruItem
class HhruSpider(scrapy.Spider):
    name = "hhru"
    start_urls = ['https://chelyabinsk.hh.ru/search/vacancy?area=113&st=searchVacancy&text=Python']

    def parse(self, response):
        tree = response.xpath('//div[@class ="vacancy-serp-item__info"]//a[@class="bloko-link HH-LinkModifier"]')
        for vacancy in tree:
            link_i = vacancy.xpath('./@href').get()
            #print(link_i) # то же что и  urljoin(response.url,link_i)
            yield response.follow(link_i, callback=self.parse_vacancy)

        next_pages = response.xpath('//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]/@href').getall()
        next_page = next_pages[-1]
        url = urljoin(response.url, next_page)
        yield response.follow(url, callback=self.parse)


    def parse_vacancy(self, response):
        my_source = 'chelyabinsk.hh.ru'
        node_i = response.xpath('//div[@class="vacancy-title "]')
        title_lst = node_i.xpath('./h1[@class="header"]/text()').extract()
        salary_lst = node_i.xpath('.//p[@class="vacancy-salary"]/text()').extract()
        link = response.url
        yield XxruItem(title=title_lst, salary=salary_lst, link=link, source=my_source)