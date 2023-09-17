import sys, os
from natsort import natsorted
from threading import Thread
from downloader import main_page, sub_page, url_check, novel_info_json_load
from pannels import DownloadPannel, ListPannel, ViewPannel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import QSize

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./img/web.png'))
        self.setWindowTitle('title')
        self.download_path = 'downloads'
        self.download_delay = 0.5
        self.mainPannel = QWidget()
        self.dp = DownloadPannel()
        self.lp = ListPannel()
        self.vp = ViewPannel()
        self.initUI()
        self.center()
    
    def initUI(self):
        #
        tabs = QTabWidget()
        tabs.addTab(self.mainPannel, 'main')
        tabs.addTab(self.vp, 'View')

        # add url lineedit
        self.dp.download_url.returnPressed.connect(self.event_btn_download)

        # add download button
        self.dp.download_btn.clicked.connect(self.event_btn_download)

        # add novellist textbrowser
        self.dp.download_list.itemDoubleClicked.connect(self.event_list_novel)
        for novel in os.listdir(self.download_path):
            self.dp.download_list.addItem(novel)

        self.lp.subtitle_list.itemDoubleClicked.connect(self.event_view_novel)

        # set Layout
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.dp)
        mainLayout.addWidget(self.lp)

        self.mainPannel.setLayout(mainLayout)

        # add statusbar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('downloader 0.0.1')

        self.setCentralWidget(tabs)
    
    def event_btn_download(self):
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

        ncode = self.dp.download_url.text()
        self.dp.download_url.clear()

        title = main_page(self.download_path, ncode)
        self.dp.download_list.addItem(title)

        donwload_thread = Thread(
            target=sub_page,
            args=(title, self.download_path, self.download_delay)
            )
        donwload_thread.daemon = True
        donwload_thread.start()

    def event_list_novel(self):
        self.lp.subtitle_list.clear()
        items = self.dp.download_list.selectedItems()
        title = items[0].text()
        novel_path = f'{self.download_path}/{title}/'
        subtitles = os.listdir(novel_path)
        for subtitle in natsorted(subtitles):
            self.lp.subtitle_list.addItem(subtitle)
        
    def event_view_novel(self, item):
        self.vp.novel_view.clear()
        subtitle = item.text()
        
        title = self.dp.download_list.selectedItems()[0].text()
        subtitle_path = f'{self.download_path}/{title}/{subtitle}'
        with open(subtitle_path, 'r', encoding='utf-8') as novel_text:
            contents = novel_text.read()
        
        self.vp.novel_view.appendPlainText(contents)
        curser = self.vp.novel_view.textCursor()
        curser.movePosition(QTextCursor.Start)
        self.vp.novel_view.setTextCursor(curser)

    def center(self):
        qRect = self.frameGeometry()
        qPoint = QDesktopWidget().availableGeometry()
        qRect.setSize(QSize(1000, 800))
        qRect.moveCenter(qPoint.center())
        self.setGeometry(qRect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
