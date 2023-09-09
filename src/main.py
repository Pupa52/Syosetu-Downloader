import sys, os
from threading import Thread
from downloader import main_page, sub_page, url_check
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./img/web.png'))
        self.setWindowTitle('title')
        self.download_path = 'downloads'
        self.download_delay = 0.5
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
        self.download_list = QTextBrowser(self)

        # set Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.download_url)
        hbox.addWidget(self.download_btn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.download_list)

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        # add statusbar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('downloader 0.0.1')

        self.setGeometry(500,500,500,500)
        self.show()
    
    def event_btn_download(self):
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

        ncode = self.download_url.text()
        self.download_url.clear()

        title = main_page(self.download_path, ncode)

        if title == '404':
            self.download_list.append(f'{ncode} is not exist')
        else:
            donwload_thread = Thread(
                target=sub_page,
                args=(title, ncode, self.download_path, self.download_delay)
            )
            donwload_thread.daemon = True
            donwload_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
