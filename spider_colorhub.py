# 导入第三方包
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 设置保存文件夹
out_dir = '/tmp/out_dir'
# 文件夹不存在则创建
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 通过循环实现多页图片的抓取
for page in range(1, 11):
    # 生成顶层图片列表页的链接
    ch_url = r'https://colorhub.me/search?tag=data&page={}'.format(page)    
    # 生成UA, 用于爬虫请求头的设置
    user_agent = UserAgent()
    # 随机生成 user agent
    ua = user_agent.random
    # 向顶层链接发送请求
    fst_response = requests.get(ch_url, headers={'User-Agent': ua})
    # 解析顶层链接的源代码
    soup = BeautifulSoup(fst_response.text, 'lxml')
    # 根据HTML的标记规则, 返回次层图片详情页的链接和图片名称
    sec_urls = [i.find('a')['href'] for i in soup.find_all(name='div', attrs={'class': 'card'})]
    pic_names = [i.find('a')['title'] for i in soup.find_all(name='div', attrs={'class': 'card'})]
    # 对每一个次层链接做循环
    for sec_url, pic_name in zip(sec_urls, pic_names):
        # 随机生成 user agent
        ua = user_agent.random
        # 向次层链接发送请求
        sec_response = requests.get(sec_url, headers={'User-Agent': ua})
        # 解析次层链接的源代码
        ch_soup = BeautifulSoup(sec_response.text, 'lxml')
        # 根据HTML的标记规则, 返回图片链接
        pic_url = 'https:' + ch_soup.find('img', {'class': 'card-img-top'})['src']
        # 对图片链接发送请求
        pic_response = requests.get(pic_url, headers={'User-Agent': ua})
        # 将二进制的图片数据写入到本地, 即存储图片到本地
        out_name = os.path.join(out_dir, pic_name)
        with open(out_name + '.jpg', mode='wb') as fn:
            fn.write(pic_response.content)

        print('download: ', out_name)
        # 生成随机秒数, 随机睡眠, 减少被封IP的情况
        seconds = random.uniform(1, 3)
        time.sleep(seconds)