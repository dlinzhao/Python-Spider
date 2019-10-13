import requests
from lxml import etree
from random import randint
from fake_useragent import UserAgent
from time import sleep as time_sleep
from prettytable import PrettyTable


def get_one_page(url, ua):
    headers = {'User-Agent': ua}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            res.encoding = res.apparent_encoding
            return res.text
    except Exception:
        return None


def parse_html(html):
    html_lxml = etree.HTML(html)
    movies = html_lxml.xpath('//div[@class="board-item-content"]')
    now_playing = []
    for mv in movies:
        name = mv.xpath('div[1]/p[@class="name"]/a/text()')[0].strip()
        star = mv.xpath('div[1]/p[@class="star"]/text()')[0].strip()
        time = mv.xpath('div[1]/p[@class="releasetime"]/text()')[0].strip()
        score = ''.join(mv.xpath('div[2]/p[@class="score"]//text()'))

        now_playing.append(dict(releasetime=time, name=name, score=score, star=star))
    
    tb = PrettyTable(["时间", "影片名称", "评分", "主演"])
    tb.padding_width = 1
    for playing in now_playing:
        tb.add_row([playing['releasetime'], playing['name'], playing['score'], playing['star']])

    print(tb)

def main(board=4, total_page=2):
    base_url = 'http://maoyan.com/board/{}?offset={}'
    user_agent = UserAgent()
    ua = user_agent.random 
    for cur_page in range(total_page):
        print("******************** 第{}页 ******************".format(cur_page + 1))
        url = base_url.format(board, cur_page*10)
        html = get_one_page(url, ua)
        parse_html(html)
        time_sleep(randint(1, 3))


if __name__ == "__main__":
    all_Lboards = {"热映口碑榜": 7, "最受期待榜": 6, "国内票房榜": 1, "北美票房榜": 2, "TOP100榜": 4}
    main()
