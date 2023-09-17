from PyQt5.QtWidgets import QWidget, QLineEdit, \
                            QPushButton, QHBoxLayout, \
                            QVBoxLayout, QListWidget, \
                            QPlainTextEdit

class DownloadPannel(QWidget):
    def __init__(self):
        super().__init__()
        self.download_url = QLineEdit(self)
        self.download_btn = QPushButton('download', self)
        self.download_list = QListWidget(self)
        self.initUI()

    def initUI(self):
        downloadLayout = QVBoxLayout()

        inputBox = QHBoxLayout()
        inputBox.addWidget(self.download_url)
        inputBox.addWidget(self.download_btn)

        downloadLayout.addLayout(inputBox)
        downloadLayout.addWidget(self.download_list)
        self.setLayout(downloadLayout)

class ListPannel(QWidget):
    def __init__(self):
        super().__init__()
        self.subtitle_list = QListWidget()
        self.initUI()

    def initUI(self):
        listLayout = QVBoxLayout()
        listLayout.addWidget(self.subtitle_list)

        self.setLayout(listLayout)

class ViewPannel(QWidget):
    def __init__(self):
        super().__init__()
        self.novel_view = QPlainTextEdit(self)
        self.initUI()
    
    def initUI(self):
        viewLayout = QVBoxLayout()
        viewLayout.addWidget(self.novel_view)

        self.setLayout(viewLayout)
