# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from pymongo import MongoClient

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python&area=113&st=searchVacancy']
    client = MongoClient('localhost', 27017)
    db = client['less5']
    coll = db.vacancy

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page,callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link,self.vacancy_parse) # по ссылке - на вакансию из списка, текст проги стоит далее

    def vacancy_parse (self, response: HtmlResponse):
        node_i = response.xpath('//div[@itemscope="itemscope"]')[0]  # разбираем отсюда
#       link_i = node_i.xpath('./meta[@itemprop="url"]/@content')[0]

        link_lst = str(node_i.xpath('./meta[@itemprop="url"]/@content')[0]).split("'")
        link = link_lst[3]

        name  = node_i.xpath('.//h1[@class="header"]/text()').extract()[0]
        source_lst = link.split('/')
        source = source_lst[2]
        salary_lst = str(node_i.xpath('.//p[@class="vacancy-salary"]/text()')[0]).split("'")
        salary = salary_lst[3]
        salary = salary.replace('\\xa0', ' ')
#        [print(x,ord(x)) for x in salary]
#        salary = "".join([x for x in salary if ord(x) !=92 & ord(x)!=127])
#        print(link, '\n', name, '\n', salary, '\n', source)


        rec = {'name': name, 'salary': salary, 'site': source, 'link': link}
        self.coll.insert_one(rec)
        yield JobparserItem(name=name, salary=salary, site=source, link=link)
