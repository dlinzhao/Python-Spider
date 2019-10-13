# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 22:37:37 2018
@author: Lonnie
需配合 selenium 以及 webdriver
"""

import os
import requests
from lxml import etree
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def download(url, fn, num=-1):
    """
    抓取特定主题
    :param url: 主题URL
    :param fn: 主题名称
    :param num: 抓取图片数量
    :return: None
    """
    is_finish = False
    if not os.path.exists('E:\\image\\{}'.format(fn)):
        os.makedirs('E:\\image\\{}'.format(fn))
    try:
        browser.execute_script("window.open()")
        browser.switch_to.window(browser.window_handles[-1])
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#waterfall')))
        cn_num = 0
        while not is_finish:
            html = etree.fromstring(browser.page_source, etree.HTMLParser())
            link = html.xpath('//*[@id="waterfall"]/div/a/@href')
            browser.execute_script("window.open()")
            browser.switch_to.window(browser.window_handles[-1])
            for lk in link:
                n_lk = 'http://huaban.com{}'.format(lk)
                fname = lk.split('/')[-2]
                fname = 'E:\\image\\{}\\{}.jpg'.format(fn, fname)
                if os.path.exists(fname):
                    print('{} exists'.format(fname))
                    continue
                try:
                    browser.get(n_lk)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#baidu_image_holder')))
                    html = etree.fromstring(browser.page_source, etree.HTMLParser())
                except Exception as e:
                    print(e)
                    continue

                sleep(randint(0, 2))
                rel_url_a = html.xpath('//*[@id="baidu_image_holder"]/a/img/@src')
                rel_url_b = html.xpath('//*[@id="baidu_image_holder"]/img/@src')
                rel_url = rel_url_a + rel_url_b
                rel_url = "http:{}".format(rel_url[0])
                print('download {}: {}'.format(fname, rel_url))
                try:
                    r = requests.get(rel_url)

                    with open(fname, 'wb') as fd:
                        fd.write(r.content)
                    cn_num += 1
                except Exception as e:
                    print(fname, e)
                    continue
            sleep(randint(1, 3))
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page"]/div[5]/div[3]/img')))
            end_img = browser.find_element_by_xpath('//*[@id="page"]/div[5]/div[3]/img')
            if 'end' in end_img.get_attribute('src') or (num != -1 and cn_num >= num):
                is_finish = True
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
    except Exception as e:
        print(e)

    
def main():
    url = 'http://huaban.com/boards/favorite/beauty'
    try:
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#waterfall')))
        html = etree.fromstring(browser.page_source, etree.HTMLParser())
        names = html.xpath('//*[@id="waterfall"]/div/a[1]/div[2]/h3/text()')
        urls = html.xpath('//*[@id="waterfall"]/div/a[1]/@href')
        for fn, u in zip(names, urls):
            main_url = 'http://huaban.com{}'.format(u)
            if '*' in fn:
                fn = fn.replace('*', '')
            download(main_url, fn)
    except Exception as e:
        print(e)
        browser.quit()
    else:
        browser.quit()

if __name__ == '__main__':
    main()
