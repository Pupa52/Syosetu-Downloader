import sys, os
import threading as th
from downloader import novel_download
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./resource/web.png'))
        self.setWindowTitle('title')
        self.workq = []
        self.initUI()
    
    def initUI(self):
        # main panel
        mainWidget = QWidget()

        # add url lineedit
        self.download_url = QLineEdit(self)
        self.download_url.returnPressed.connect(self.event_btn_download)

        # add download button
        self.download_btn = QPushButton('download', self)
        self.download_btn.clicked.connect(self.event_btn_download)

        # add novellist textbrowser
        self.download_log = QTextBrowser(self)
        novel_list = os.listdir('./downloads')
        for novel in novel_list:
            self.download_log.append(novel)

        # set Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.download_url)
        hbox.addWidget(self.download_btn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.download_log)

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        # add statusbar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('downloader 0.0.1')

        self.setGeometry(500,500,500,500)
        self.show()
    
    def event_btn_download(self):
        ncode = self.download_url.text()
        self.download_url.clear()

        thread1 = th.Thread(target=novel_download, args=(ncode,))
        thread1.setDaemon(True)
        thread1.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
