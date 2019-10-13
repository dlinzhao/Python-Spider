import requests
from random import randint
from urllib.parse import urlencode
from time import sleep as time_sleep
from fake_useragent import UserAgent
from pyquery import PyQuery

def generate_headers():
    user_agent = UserAgent()
    ua = user_agent.random 
    # 构造异步请求头
    headers = {
        'Host': 'm.weibo.cn',
        'Referer': 'https://m.weibo.cn',
        'User-Agent': ua,
        'X-Requested-With': 'XMLHttpRequest'
    }

    return headers

def get_page(page=1):
    headers = generate_headers()
    base_url = 'https://m.weibo.cn/api/container/getIndex?'
    # 构造异步请求参数
    params = {
        'containerid': "102803",
        'openApp': 0,
        'since_id': page
    }   
    try:
        # 通过requests的get方法传递异步请求参数
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json_data):
    if json_data:
        item_datas = json_data['data']['cards']
        for item in item_datas:
            item_blog = item['mblog']
            weibo = {}
            weibo['id'] = item_blog['id']
            weibo['text'] = PyQuery(item_blog['text']).text()
            weibo['attitudes'] = item_blog['attitudes_count']
            weibo['reposts'] = item_blog['reposts_count']
            yield weibo


if __name__ == "__main__":
    for page in range(1, 11):
        json_data = get_page(page)
        results = parse_page(json_data)
        for result in results:
            print(result)
