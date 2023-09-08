import requests
import json
import time
import os
from bs4 import BeautifulSoup

def url_request(url):
    try:
        res = requests.get(url, timeout=5.0, headers={'User-Agent':'Mozilla/5.0'})
        if res.status_code == 200:
            return res.text
        return res.status_code
    except requests.exceptions.Timeout:
        print(f'{url} request time out')

# novel main page download function 
def main_page(url):
    html = url_request(url)
    if html == 404:
        return 404
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('p', class_='novel_title').get_text()
    writer = soup.find('div', class_='novel_writername').find('a').get_text()
    sublist = soup.select_one('div.index_box').select('dl.novel_sublist2')

    # novel infomation dictionary to create json
    novel_info = {
        'url' : url,
        'title' : title,
        'writer' : writer,
        'max_page' : len(sublist),
        'page' : {}
    }

    # save each subpage infomation
    for i, subtitle in enumerate(sublist):
        novel_info['page'][i + 1] = {
            'subtitle_title' : subtitle.select_one('dd.subtitle > a').get_text(),
            'subtitle_url' : subtitle.select_one('dd.subtitle > a').get('href'),
            'subtitle_update' : subtitle.select_one('dt.long_update').get_text(),
        }

    # download folder create
    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    # download novel folder create
    directory_name = f'downloads/{title}'
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    # novel infomation json.dump
    novel_json_path = directory_name + '/' + title + '.json'
    with open(novel_json_path, 'w', encoding='utf-8') as novel_json:
        json.dump(novel_info, novel_json, ensure_ascii=False, indent=4)

    return title

# novel sub page download function
def sub_page(title):

    # novel infomation json.load
    novel_json_path = f'downloads/{title}/{title}.json'
    with open(novel_json_path, 'r', encoding='utf-8') as novel_json:
        novel_info = json.load(novel_json)

    # https://syosetu.com/
    url = novel_info['url'] + '/'

    # novel subpage infomation dictionary
    pages = novel_info['page']

    for page in pages.keys():
        print(f'{title} : {page}')
        html = url_request(url + page)
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.select_one('p.novel_subtitle')
        contents = soup.select('#novel_honbun > p')

        file_name = 'downloads/' + novel_info['title'] + '/' + page + '_' + title.get_text() + '.txt'

        content_text = title.get_text().strip() + '\n'
        for content in contents:
            content_text += content.get_text().strip() + '\n'

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content_text)

        # delay 0.5
        time.sleep(0.5)

def check_url(ncode: str):
    if ncode.startswith('https://ncode.syosetu.com/'):
        url = ncode
    elif ncode.startswith('/'):
        url = 'https://ncode.syosetu.com' + ncode
    else:
        url = 'https://ncode.syosetu.com/' + ncode
    return url
