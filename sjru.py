# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from jobparser.items import XxruItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response):
        tree = response.xpath('//div[@style="display:block"]//a[@target="_blank"]')  # body
        for vacancy in tree:
            link_i = urljoin(response.url, vacancy.xpath('@href').get())
            yield response.follow(link_i, callback=self.parse_vacancy)

        next_pages = response.xpath('//div[@class ="L1p51"]//a[@target="_self"]/@href').getall()
        next_page = next_pages[-1]
        url = urljoin(response.url, next_page)
        yield response.follow(url, callback=self.parse)

    def parse_vacancy(self, response):
        my_source = "www.superjob.ru"
        link       = response.url
        title_lst  = response.xpath('//h1[@class]/text()').extract()
        salary_lst = response.xpath('//h1[@class]/following-sibling::span').extract()
#        print('SjruSpider: salary_lst=',salary_lst)
        yield XxruItem(title=title_lst, salary=salary_lst, link=link, source=my_source)


