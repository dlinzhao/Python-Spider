# -*- coding: utf-8 -*-
"""
爬取 UCL 的强化学习课件
"""
import urllib.request as Request
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import re


# http://www0.cs.ucl.ac.uk/staff/D.Silver/web/Teaching_files/intro_RL.pdf
url = 'http://www0.cs.ucl.ac.uk/staff/D.Silver/web/Teaching.html'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
 Chrome/67.0.3396.99 Safari/537.36'}

req = Request.Request(url=url, headers=headers)
html = Request.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'lxml')
lectures = soup.select("p.paragraph_style_1 > a")

for lecture in lectures:
    if lecture['title'].startswith('Teaching_files'):
        print(lecture.string)
        url = 'http://www0.cs.ucl.ac.uk/staff/D.Silver/web/' + lecture['href']
        Request.urlretrieve(url, './RL/{}.pdf'.format(lecture.string))
    sleep(randint(0, 3))
