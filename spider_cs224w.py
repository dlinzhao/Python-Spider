import os
import time
import random
import requests
from lxml import etree
from fake_useragent import UserAgent


def download_item(url, ua, type_='txt'):
    headers = {'User-Agent': ua}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            res.encoding = res.apparent_encoding
            return res.text if type_ == 'txt' else res.content
    except Exception:
        return None

def download():
    base_url = 'http://web.stanford.edu/class/cs224w/'
    user_agent = UserAgent()
    ua = user_agent.random 

    html = download_item(base_url, ua)
    if html is None:
        print('Request failed!')
        return
    text  = etree.HTML(html)
    links = text.xpath('//*[@id="schedule"]/table/tbody/tr/td/a/@href')
    for s in links:
        if not s.startswith('slides'):
            continue
        cont = download_item(base_url + s, ua, type_='bin')
        if cont is None:
            print('Download fail: ', s)
            continue
        name = s.split('/')[-1]
        print('Downloaded: ', name)
        with open(name, 'wb') as fd:
            fd.write(cont.content)
        time.sleep(random.randint(0,3))


if __name__ == "__main__":
    download()
