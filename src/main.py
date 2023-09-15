import sys, os
from threading import Thread
from downloader import main_page, sub_page, url_check
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./img/web.png'))
        self.setWindowTitle('title')
        self.download_path = 'downloads'
        self.download_delay = 0.5
        self.initUI()
        self.center()
    
    def initUI(self):
        # main panel
        mainPannel = QWidget()
        downlaodPannel = QWidget()
        listPannel = QWidget()

        # add url lineedit
        self.download_url = QLineEdit(self)
        self.download_url.returnPressed.connect(self.event_btn_download)

        # add download button
        self.download_btn = QPushButton('download', self)
        self.download_btn.clicked.connect(self.event_btn_download)

        # add novellist textbrowser
        # self.download_list = QTextBrowser(self)
        self.download_novel_list = QListWidget(self)
        self.download_novel_list.itemDoubleClicked.connect(self.event_list_novel)
        for novel in os.listdir(self.download_path):
            self.download_novel_list.addItem(novel)

        self.novel_sub_list = QListWidget(self)

        # set Layout - download pannel
        downloadLayout = QVBoxLayout()

        inputBox = QHBoxLayout()
        inputBox.addWidget(self.download_url)
        inputBox.addWidget(self.download_btn)

        downloadLayout.addLayout(inputBox)
        downloadLayout.addWidget(self.download_novel_list)

        downlaodPannel.setLayout(downloadLayout)

        # set Layout - list pannel
        listLayout = QVBoxLayout()
        listLayout.addWidget(self.novel_sub_list)

        listPannel.setLayout(listLayout)

        # set Layout
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(downlaodPannel)
        mainLayout.addWidget(listPannel)

        mainPannel.setLayout(mainLayout)
        self.setCentralWidget(mainPannel)

        # add statusbar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('downloader 0.0.1')
    
    def event_btn_download(self):
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

        ncode = self.download_url.text()
        self.download_url.clear()

        title = main_page(self.download_path, ncode)
        self.download_novel_list.addItem(title)

        donwload_thread = Thread(
            target=sub_page,
            args=(title, ncode, self.download_path, self.download_delay)
            )
        donwload_thread.daemon = True
        donwload_thread.start()

    def event_list_novel(self):
        items = self.download_novel_list.selectedItems()
        items[0].text

    def center(self):
        qRect = self.frameGeometry()
        qPoint = QDesktopWidget().availableGeometry()
        qRect.setSize(QSize(1000, 600))
        qRect.moveCenter(qPoint.center())
        self.setGeometry(qRect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
