from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import requests
from bs4 import BeautifulSoup

URL = "https://kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese%2F"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')

animeLinks = []
animeNames = []
table = soup.find('table', attrs = {'id':'flisttable'})
for row in table.findAll('td', attrs = {'class':''}):
    animeURL = row.a['href']
    anime = row.find("strong").text
    animeNames.append(anime)
    animeLinks.append('https://kitsunekko.net/' + animeURL)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Kitsunekko Crawler")
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        self.animeIndex = 0

        # 0 = all, 1 = SRT, 2 = ASS, 3 = ZIP
        self.downloadIndicator = 0
        self.fileName = "subs.srt"
        self.subtitleLinks = []

        layout = QVBoxLayout()
        animeNameLabel = QLabel("Select Anime: ")
        downloadAllbutton = QPushButton("Download All Files")
        downloadAllbutton.clicked.connect(self.downloadAll)
        downloadSRTbutton = QPushButton("Download SRT Files")
        downloadSRTbutton.clicked.connect(self.setSRT)
        downloadSRTbutton.clicked.connect(self.downloadAll)
        downloadASSbutton = QPushButton("Download ASS Files")
        downloadASSbutton.clicked.connect(self.setASS)
        downloadASSbutton.clicked.connect(self.downloadAll)
        downloadZIPbutton = QPushButton("Download ZIP and RAR Files")
        downloadZIPbutton.clicked.connect(self.setZIP)
        downloadZIPbutton.clicked.connect(self.downloadAll)

        comboBoxAnimeNames = QComboBox()
        comboBoxAnimeNames.addItems(animeNames)
        comboBoxAnimeNames.currentIndexChanged.connect(self.index_changed)
        layout.addWidget(animeNameLabel)
        layout.addWidget(comboBoxAnimeNames)
        layout.addWidget(downloadAllbutton)
        layout.addWidget(downloadSRTbutton)
        layout.addWidget(downloadASSbutton)
        layout.addWidget(downloadZIPbutton)

        comboBoxAnimeNames = QWidget()
        comboBoxAnimeNames.setLayout(layout)

        self.setCentralWidget(comboBoxAnimeNames)

    def index_changed(self, i):  # i is an int
        self.animeIndex = i

    def downloadAll(self):
        URL = animeLinks[self.animeIndex]
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.subtitleLinks = []
        table = soup.find('table', attrs={'id': 'flisttable'})
        for row in table.findAll('td', attrs={'class': ''}):
            subtitle = row.a['href']
            self.subtitleLinks.append('https://kitsunekko.net/' + subtitle)

        for i in range(len(self.subtitleLinks)):
            if self.downloadIndicator == 1 or self.downloadIndicator == 0:
                if self.subtitleLinks[i].rsplit('.', 1)[-1] == 'srt':
                    self.downloadSRT(i)
            if self.downloadIndicator == 2 or self.downloadIndicator == 0:
                if self.subtitleLinks[i].rsplit('.', 1)[-1] == 'ass':
                    self.downloadASS(i)
            if self.downloadIndicator == 3 or self.downloadIndicator == 0:
                if self.subtitleLinks[i].rsplit('.', 1)[-1] == 'zip' or self.subtitleLinks[i].rsplit('.', 1)[-1] == 'rar' or self.subtitleLinks[i].rsplit('.', 1)[-1] == '7z':
                    self.downloadZIP(i)

    def downloadSRT(self, i):
        fileName = self.subtitleLinks[i].rsplit('/', 1)[-1]
        r = requests.get(self.subtitleLinks[i], stream=True)
        with open(fileName, "wb") as srt:
            srt.write(r.content)

    def downloadASS(self, i):
        fileName = self.subtitleLinks[i].rsplit('/', 1)[-1]
        r = requests.get(self.subtitleLinks[i], stream=True)
        with open(fileName, "wb") as ass:
            ass.write(r.content)

    def downloadZIP(self, i):
        fileName = self.subtitleLinks[i].rsplit('/', 1)[-1]
        r = requests.get(self.subtitleLinks[i], stream=True)
        with open(fileName, "wb") as code:
            code.write(r.content)

    def setSRT(self):
        self.downloadIndicator = 1

    def setASS(self):
        self.downloadIndicator = 2

    def setZIP(self):
        self.downloadIndicator = 3



app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
