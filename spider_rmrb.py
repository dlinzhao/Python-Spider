# _*_ coding: utf-8
"""
爬取人民日报，需要登陆后配置cookies，不能爬取太快，否则封ip地址
config.txt 放在同级目录下，里面内容是登陆后的cookies
"""

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import requests
import random
import os
import time

user_agent = [
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
]


def GetPageNumber(date):
    the_first_page = u'http://data.people.com.cn/rmrb/%s/1' % (date)
    url = the_first_page
    try:
        html = urlopen(url).read()
    except:
        return 0
    soup = bs(html, "lxml")
    return int(soup.find(id='UseRmrbPageNum').string)


def GetAllEssaysWeb(date):
    essay_web_list = []
    page_number = GetPageNumber(date)
    if page_number == 0:
        return []
    print(page_number)
    for n in range(1, (page_number + 1)):
        time.sleep(random.randint(1, 3))
        the_page = u'http://data.people.com.cn/rmrb/%s/%s' % (date, n)
        the_date = u'%s' % (date)
        url = the_page
        try:
            html = urlopen(url).read()
        except:
            continue
        soup = bs(html, "lxml")
        H3_tags = soup.find_all("h3")
        for Tags in H3_tags:
            Tags_content = Tags.contents
            if len(Tags_content) > 1:
                Target_tags = Tags_content[1]
                Hrefs = Target_tags.get('href')
                if len(Hrefs) > 20:
                    essay_web_part = Hrefs
                    essay_web = u'http://data.people.com.cn%s' % (essay_web_part)
                    if essay_web[31:39] == the_date:
                        if essay_web not in essay_web_list:
                            essay_web_list.append(essay_web)
    print(the_date, len(essay_web_list))
    return essay_web_list


#### Extract Text
def GetText(soup):
    text_titles = GetTitle(soup)
    text_dates = GetDate(soup)
    text_body = GetBody(soup)
    text = u'%s\n%s\n%s' % (text_titles, text_dates, text_body)
    return text


def GetTitle(soup):  ### Change
    main_title = u'None'
    MT = soup.find_all("div", class_="title")
    for mt in MT:
        mt_strings = mt.stripped_strings
        for mt_string in mt_strings:
            main_title = u'%s' % (mt_string)
    ST = soup.find_all("div", class_="subtitle")
    sub_title = u'None'
    for st in ST:
        st_strings = st.stripped_strings
        for st_string in st_strings:
            sub_title = u'%s' % (st_string)
    titles = u'标题：%s\n副标题：%s' % (main_title, sub_title)
    return titles


def GetDate(soup):  # Change
    dates = u'版面：'
    date_tags = soup.find_all("div", class_="sha_left")
    for date_tag in date_tags:
        date_strings = date_tag.stripped_strings
        for date_string in date_strings:
            dates += u'%s ' % (date_string)
    # dates = re.sub('\s','',dates)
    return dates


def GetBody(soup):
    text_list = []
    whole_body = u'正文：\n'
    parts = soup.find_all("p")
    for part in parts:
        body = part.string
        if body not in text_list:
            text_list.append(body)
            whole_body += u'%s\n' % (body)
    return whole_body


def main(date, cookies):
    # lock.acquire()
    root_dir = r'D:\spider'
    dst_dir = os.path.join(root_dir, date[:6])
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    webs = GetAllEssaysWeb(date)
    global user_agent
    headers = {'user-agent': user_agent[random.randint(0, len(user_agent) - 1)]}
    for web in webs:
        time.sleep(random.randint(2, 5))
        url = web
        try:
            html = requests.get(url=url, headers=headers, cookies=cookies)
        except:
            continue
        html.encoding = 'utf-8'
        html = html.text
        soup = bs(html, "lxml")
        the_essay = GetText(soup)
        the_text = u'%s\n\n\n' % (the_essay)
        fn_address = r'{}.txt'.format(os.path.join(dst_dir, date))
        fn = open(fn_address, 'a')
        fn.write(the_text)
        fn.close()
    # lock.release()


if __name__ == '__main__':
    cur_dir = os.curdir
    if not os.path.exists(os.path.join(cur_dir, 'config.txt')):
        print('Not find config.txt')
        sys.exit(-1)

    cookies = {}
    with open('config.txt', 'r') as fd:
        line = fd.readlines()
    lines = line[0].split(';')
    for kv in lines:
        key, val = kv.split('=')
        key = key.strip()
        val = val.strip()
        cookies[key] = val
    #    print(cookies)
    year_input = input("Input the year in the form like '2016': ")
    month_input = input("Input the month in the form like '01': ")
    day_input = input("Input the start day in the form like '01': ")
    date = ['{:02d}'.format(x) for x in range(int(day_input), 32)]
    dst = ['{}{}{}'.format(year_input, month_input, x) for x in date]
    # Process(target=main, args=(lock, d, dst_dir)).start()
    #    p = Pool(20)
    #    p.map(main, dst)
    for d in dst:
        main(d, cookies)
