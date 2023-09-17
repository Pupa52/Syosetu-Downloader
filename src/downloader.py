import json
import time
import os
import requests
from bs4 import BeautifulSoup

def url_request(url) -> str:
    try:
        res = requests.get(url, timeout=5.0, headers={'User-Agent':'Mozilla/5.0'})
        if res.status_code == 200:
            return res.text
    except requests.exceptions.Timeout:
        print(f'{url} request time out')
    return str(res.status_code)

def url_check(ncode: str) -> str:
    if ncode.startswith('https://ncode.syosetu.com/'):
        url = ncode
    elif ncode.startswith('/'):
        url = 'https://ncode.syosetu.com' + ncode
    else:
        url = 'https://ncode.syosetu.com/' + ncode
    return url

# novel main page download function
def main_page(download_path, ncode: str) -> str:
    url = url_check(ncode)
    html = url_request(url)

    if html == '404':
        return html

    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('p', class_='novel_title').get_text()
    writer = soup.find('div', class_='novel_writername').find('a').get_text()
    sublist = soup.select_one('div.index_box').select('dl.novel_sublist2')

    # novel infomation dictionary to create json
    novel_info = {
        'url' : url + '/',
        'ncode' : ncode,
        'title' : title,
        'writer' : writer,
        'max_page' : len(sublist),
        'page' : {}
    }

    # save each subpage infomation
    for i, subtitle in enumerate(sublist, start=1):
        novel_info['page'][i] = {
            'subtitle_title' : subtitle.select_one('dd.subtitle > a').get_text(),
            'subtitle_url' : subtitle.select_one('dd.subtitle > a').get('href'),
            'subtitle_update' : subtitle.select_one('dt.long_update').get_text(),
        }

    # download novel folder create
    download_path = download_path + '/' + title
    print(download_path)
    if not os.path.exists(download_path):
        os.makedirs(download_path, exist_ok=True)

    # novel infomation json.dump
    novel_json_path = f'{download_path}/novel_info.json'
    novel_info_json_dump(novel_json_path, novel_info)

    return title

# novel sub page download function
def sub_page(title, download_path, download_delay) -> None:
    # novel infomation json.load
    download_path = download_path + '/' + title
    novel_json_path = f'{download_path}/novel_info.json'
    novel_info = novel_info_json_load(novel_json_path)

    url = novel_info['url'] # title url
    pages = novel_info['page'] # subtitle dict

    for page in pages.keys():
        html = url_request(url + page)
        soup = BeautifulSoup(html, 'html.parser')

        subtitle = soup.select_one('p.novel_subtitle').get_text().strip()
        contents = soup.select('#novel_honbun > p')

        novel_text = subtitle + '\n'
        for line in contents:
            novel_text += line.get_text().strip() + '\n'

        file_name = f'{download_path}/{page}_{subtitle}.txt'
        with open(file_name, 'w', encoding='utf-8') as novel_text_file:
            novel_text_file.write(novel_text)

        time.sleep(download_delay)

def novel_info_json_dump(novel_json_path, novel_info) -> None:
    with open(novel_json_path, 'w', encoding='utf-8') as novel_json:
        json.dump(novel_info, novel_json, ensure_ascii=False, indent=4)

def novel_info_json_load(novel_json_path) -> json:
    with open(novel_json_path, 'r', encoding='utf-8') as novel_json:
        novel_info = json.load(novel_json)
    return novel_info
