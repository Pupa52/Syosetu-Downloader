from downloader import novel_download
import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [
    [sg.Text('Input url or code'), sg.InputText()],
    [sg.Text('ex)https://ncode.syosetu.com/aaaaaa/ or aaaaaa')]
    [sg.Button('Ok'), sg.Button('Cancel')]
]

if __name__ == '__main__':
    window = sg.Window('Syosetu Downloader', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSE or event == 'Cancel':
            break
        print()