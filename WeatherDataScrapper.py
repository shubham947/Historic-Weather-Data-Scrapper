# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import logging
import json

country = 'india'
city = 'kolkata'
class WeatherhistorySpider(scrapy.Spider):
    name = 'WeatherHistory'
    allowed_domains = ['timeanddate.com']
    start_urls = ['https://timeanddate.com/weather/' + country + '/' + city + '/historic']

    def parse(self, response):
        prev_months = response.xpath('//*[@id="month"]/option/@value').extract()
        for month in prev_months:
            y = month.split('-')[0]
            m = month.split('-')[1].strip('0')
            next_url = response.request.url + '?month=' + m + '&year=' + y
            # print(next_url)
            yield Request(next_url, callback=self.parse_weather)
    
    def parse_weather(self, response):
        month_data = response.xpath('//*/script[@type="text/javascript"]/text()').extract()[1].split(';')[0].split('=')[1]
        parsed_month = (json.loads(month_data))
        # print(json.dumps(parsed_month, indent=4, sort_keys=True))
        for row in parsed_month['detail']:
            yield {
                "date": row['ds'].split(',')[1].lstrip(),
                "day": row['ds'].split(',')[0],
                "time": row['ts'],
                "maxTemp": row['temp'],
                "minTemp": row['templow'],
                "baro": row['baro'],
                "windSpeed": row['wind'],
                "windDir": row['wd'],
                "humidity": row['hum']
            }