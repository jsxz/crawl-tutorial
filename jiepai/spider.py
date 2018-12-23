# coding:utf8
import json
import re
import pymongo
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
from jiepai.config import *

client =pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        print('请求索引页出错了')
        return None
def parse_page_index(html):
    data = json.loads(html)
    print(data)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')
def get_page_detail(url):
    try:
        res = requests.get(url)
        if res.status_code==200:
            return res.text
        return None
    except RequestException:
        print('请求详细页出错',url)
        return None
def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    print(html)
    title = soup.select('title')[0].get_text()
    print(title)
    images_pat = re.compile('var gallery = (.*?);', re.S)
    result = re.search(images_pat, html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            return {
                'title':title,
                'url':url,
                'images':images
            }
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongodb成功')
        return True
    return False

def main():
    html = get_page_index(0, '街拍')
    print(html)
    # for url in parse_page_index(html):
    #     html = get_page_detail(url)
    #     print(html)
        # if html:
        #     result = parse_page_detail(html,url)
        #     save_to_mongo(result)
if __name__=='__main__':
    main()