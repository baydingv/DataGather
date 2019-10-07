# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['sj.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&without_agencies=1&geo%5Bc%5D%5B0%5D=1&page=1']

    def parse(self, response: HtmlResponse):
        node_i = response.xpath('//div[@style="display:block"]//a[@target="_blank"]')  # список нужных элементов
        source = 'superjob.ru'
        for en in node_i:
            link_en = en.xpath('@href').get()
            link = "".join(['http://',source,str(link_en)])
            yield response.follow(link,self.vacancy_parse) # по ссылке - на вакансию из списка, текст проги стоит далее


    def vacancy_parse (self, response: HtmlResponse):
        print('------------- in vacancy_parse --------------')
        name_path = response.xpath('.//h1[@class]').get()
        name = name_path.xpath('./text()').get()
        print("name = ",name)
        salary_path = name_path.xpath('./following-sibling::span').get()
        salary_base = salary_path.xpath('./text()').get()
        salary = salary_base
        salary_add_path = salary_path.xpath('./child::span')
        for sal_en in salary_add_path:
            salary = " ".join([salary,sal_en.xpath('./text()')[0] ])

        yield JobparserItem(name=name, salary=salary, site=source, link=link)
