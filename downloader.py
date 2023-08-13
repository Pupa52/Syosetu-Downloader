from bs4 import BeautifulSoup
import requests
import json
import os
import time

def url_request(url):

    res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})

    if res.status_code == 200:
        return res.text
    else:
        return res.raise_for_status()

def main_page(url):

    html = url_request(url)
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('p', class_='novel_title').get_text()
    writer = soup.find('div', class_='novel_writername').find('a').get_text()
    subtitle_list = soup.select_one('div.index_box').select('dl.novel_sublist2')

    novel_info = {
        'url' : url,
        'title' : title,
        'writer' : writer,
        'max_page' : len(subtitle_list),
        'page' : {}
    }

    for i, st in enumerate(subtitle_list):
        novel_info['page'][i + 1] = {
            'subtitle_title' : st.select_one('dd.subtitle > a').get_text(),
            'subtitle_url' : st.select_one('dd.subtitle > a').get('href'),
            'subtitle_update' : st.select_one('dt.long_update').get_text(),
        }

    directory_name = f'{title}'

    try:
        os.mkdir(directory_name)
    except FileExistsError:
        print(f'Directory {directory_name} already exists.')
    except Exception as e:
        print(f'An error occurred: {e}')

    novel_path = directory_name + '/' + title + '.json'
    with open(novel_path, 'w', encoding='utf-8') as novel_json:
        json.dump(novel_info, novel_json, ensure_ascii=False, indent=4)
    
    return title

def sub_page(title):

    novel_json_path = f'{title}/{title}.json'

    with open(novel_json_path, 'r', encoding='utf-8') as novel_json:
        novel_info = json.load(novel_json)

    url = novel_info['url'] + '/'
    novel_sublist = novel_info['page']

    for i in novel_sublist.keys():

        html = url_request(url + i)
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.select_one('p.novel_subtitle')
        honbun = soup.select('#novel_honbun > p')

        file_name = novel_info['title'] + '/' + i + '_' + novel_sublist[i]['subtitle_title'] + '.txt'

        with open(file_name, 'w', encoding='utf-8') as f:
            honbun_text = title.get_text().strip() + '\n'
            for h in honbun:
                honbun_text += h.get_text().strip() + '\n'
            f.write(honbun_text)

        print(f'number {i} complete')
        time.sleep(0.1)

def novel_download(novel_code: str):
    if novel_code.startswith('https://ncode.syosetu.com'):
        url = novel_code
    elif novel_code.startswith('/'):
        url = 'https://ncode.syosetu.com' + novel_code
    else:
        url = 'https://ncode.syosetu.com/' + novel_code

    title = main_page(url)
    sub_page(title)

if __name__ == '__main__':
    while True:
        print('Input url or novel_code')
        print('ex)https://ncode.syosetu.com/aaaaaa/ or aaaaaa')
        novel_code = input('>')

        novel_download(novel_code)