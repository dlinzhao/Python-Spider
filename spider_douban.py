"""
爬取豆瓣当前正在热映的电影
"""
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import sys
import os

user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) \
    Version/5.1 Safari/534.50'


def main(url, headers):
    try:
        html = requests.get(url=url, headers=headers)
        html.raise_for_status()
        html.encoding = 'utf-8'
    except:
        sys.exit(-1)
    soup = BeautifulSoup(html.text, 'lxml')
    movies = soup.select('#nowplaying > div.mod-bd > ul')
    movies = movies[0].find_all('li')
    now_playing = []
    for mov in movies:
        mv = {}
        if 'list-item' in mov.attrs['class']:
            mv['data-release'] = mov.attrs['data-release']
            mv['data-region'] = mov.attrs['data-region']
            mv['data-title'] = mov.attrs['data-title']
            mv['data-score'] = mov.attrs['data-score']
            mv['data-star'] = mov.attrs['data-star']
            mv['data-director'] = mov.attrs['data-director']
            mv['data-actors'] = mov.attrs['data-actors']
            mv['data-duration'] = mov.attrs['data-duration']
            now_playing.append(mv)

    tb = PrettyTable(["时间", "地区", "影片名称", "评分", "star", "时长"])
    tb.padding_width = 1
    for playing in now_playing:
        tb.add_row([playing['data-release'], playing['data-region'], playing['data-title'],
                    playing['data-score'], int(playing['data-star']) / 10, playing['data-duration']])

    print(tb)


if __name__ == '__main__':
    url = r'https://movie.douban.com/cinema/nowplaying/'
    headers = {'User-Agent': user_agent}
    while True:
        city = input('input a city e.g. wuhan:')
        if city == 'exit':
            break
        n_url = url + city
        main(n_url, headers)
        print('type exit if you want end it!')
    os.system("pause")
