import requests
import lxml.etree

# test code in local machine
url = 'E:\经典影片_电影大全_经典高清电影-猫眼电影.html'
html = ''
with open(url, 'r', encoding='utf-8') as fp:
    html = fp.read()

selector = lxml.etree.HTML(html)

movies = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/dl/dd')
print(len(movies))
for movie in movies:
    name = movie.xpath('./div[2]/a/text()')[0]
    time = list(movie.xpath('./div[1]/div[2]/a/div/div[4]/text()'))[1].strip()
    type_m = list(movie.xpath('./div[1]/div[2]/a/div/div[2]/text()'))[1].strip()
    print(name)
    print(time)
    print(type_m)
    break
