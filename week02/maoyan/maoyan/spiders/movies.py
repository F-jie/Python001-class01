import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films?showType=3']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for movie in movies[:10]:
            name = movie.xpath('./div/@title')[0].extract().strip()
            eles = movie.xpath(f'//div[@title="{name}"]')
            type_m = eles[1].xpath('./text()')[1].extract().strip()
            time = eles[3].xpath('./text()')[1].extract().strip()
            item = MaoyanItem()

            item['name'] = name
            item['time'] = time
            item['type_m'] = type_m
            yield item
