import scrapy
import json

class VotesSpider(scrapy.Spider):
    name = 'votes'

    def start_requests(self):
        urls = [
            'http://www.tucamarapr.org/dnncamara/web/actividadlegislativa/votaciones.aspx?mNumber=0&body=&legType=&option=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'measures_data.json'
        measures_data = []

        measure_holders = response.css('li.active div.holder')

        for item in measure_holders:
            data = {
                'medida': item.css('span.measure-name a::text').re('\w+.*')[0],
                'data': item.css('span.measure-name span::text').re('\w+.*'),
                'autor': item.css('span.author a::text').re('\w+.*'),
            }
            measures_data.append(data)
            
        with open(filename, 'w') as data_file:
            json.dump(measures_data, data_file, indent=2)
        
        self.log('Saved file %s' % filename)