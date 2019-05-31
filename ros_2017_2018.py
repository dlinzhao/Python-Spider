"""
爬取 ROS Summer 2017,2018 的课件
"""
import os
import sys
import time
import random
import requests
import bs4
from bs4 import BeautifulSoup


user_agent = [
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
]


def main(url_addr, file_path, useragent):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    headers = {'User-Agent': useragent[random.randint(0, len(useragent) - 1)]}
    try:
        html = requests.get(url=url_addr, headers=headers)
        # html.raise_for_status()
        html.encoding = 'utf-8'
    except requests.HTTPError:
        print('error ....')
        sys.exit(1)

    ref_url = url_addr[:-9]
    soup = BeautifulSoup(html.text, 'lxml')
    td_list = soup.find_all('td')
    td_a = [td for td in td_list if td.a]
    for td in td_a:
        fname = td.contents[0]
        if isinstance(fname, bs4.Tag):
            fname = fname.string
        fname = fname.strip()
        list_a = td.find_all('a')
        for i, a in enumerate(list_a):
            href = a['href']
            if not href.endswith('.pdf'):
                continue
            if os.path.exists(os.path.join(file_path, '{}_{}.pdf'.format(fname, i))):
                print("exist {}_{}.pdf ...".format(fname, i))
                continue
            time.sleep(random.randint(2, 5))
            headers = {'User-Agent': useragent[random.randint(0, len(useragent) - 1)]}
            url_addr = ref_url + href
            try:
                html = requests.get(url=url_addr, headers=headers)
                if html.status_code != 200:
                    continue
                # html.raise_for_status()
                with open(os.path.join(file_path, '{}_{}.pdf'.format(fname, i)), 'wb') as fd:
                    fd.write(html.content)
                print("download {}_{}.pdf finish ...".format(fname, i))
            except requests.HTTPError:
                print('download {}_{} error ....'.format(fname, i))


if __name__ == '__main__':
    url_2017 = r'http://www.roseducation.org/ros2017/prog.html'
    url_2018 = r'http://www.roseducation.org/ros2018/prog.html'
    # main(url_2017, r'E:\book\ROS\2017_ROS_Summer_School', user_agent)
    main(url_2018, r'E:\book\ROS\2018_ROS_Summer_School', user_agent)
