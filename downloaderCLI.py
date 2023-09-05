from downloader import novel_download

if __name__ == '__main__':
    while True:
        print('Input url or novel_code')
        print('ex)https://ncode.syosetu.com/aaaaaa/ or aaaaaa')
        novel_code = input('Input> ')

        novel_download(novel_code)
