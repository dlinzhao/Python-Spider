"""
爬取华东师范大学数学系LaTeX教程
"""
import requests
from bs4 import BeautifulSoup
import os

save_dir = './tex'
cur_dir = os.getcwd()
dst_dir = os.path.join(cur_dir, save_dir)
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

url = 'http://math.ecnu.edu.cn/~latex/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

html = requests.get(url=url, headers=headers)
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.text, 'lxml')
list_td_a = soup.select('td.td3 > a')

for td in list_td_a:
    link = td['href']
    filename = link.split('/')[-1]
    if not filename.endswith('.tex') or not filename.endswith('.pdf'):
        continue
    if os.path.exists(os.path.join(dst_dir, filename)):
        continue
    sub_url = url + link
    print('{}\t{}'.format(filename, sub_url))
    file = requests.get(url=sub_url, headers=headers)
    with open(os.path.join(dst_dir, filename), 'wb') as fd:
        fd.write(file.content)
