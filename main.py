import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import requests
import webbrowser
import clipboard

from requests.api import get, head
from mojang import MojangAPI
import datetime

form_class = uic.loadUiType("mainPage.ui")[0]

class MainWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.lineEdit.returnPressed.connect(self.getname)
        self.pushButton.clicked.connect(QtWidgets.qApp.quit)
        self.pushButton_2.clicked.connect(self.showMinimized)
        self.pushButton_3.clicked.connect(self.OK)
        self.pushButton_6.clicked.connect(self.NO_PIC)
        self.pushButton_5.clicked.connect(self.NO)
        self.pushButton_4.clicked.connect(self.WHITELIST)
        self.listWidget.itemDoubleClicked.connect(self.listClick)
        self.show()

    def listClick(self):
        str = self.listWidget.currentItem().text()
        data = str.split(' - ')

        date_1 = data[1].split('-')
        
        if (self.listWidget.currentRow() != 0):
            prestr = self.listWidget.item(self.listWidget.currentRow() - 1).text()
            predata = prestr.split(' - ')
            date_2 = predata[1].split('-')

            url_1 = "https://section.cafe.naver.com/ca-fe/home/search/articles?q=" + data[0]
            url_2 = url_1 + "&em=1&pr=7&ps=" + date_1[0] + "." + date_1[1] +"." + date_1[2] + "&pe=" + date_2[0] + "." + date_2[1] +"." + date_2[2]
            url_4 = url_2 + "&in=신고%20경고%20추방%20벤%20테러%20절도%20약탈%20욕설%20핵%20엑스레이%20매크로"
        else:
            current_time = datetime.date.today()
            time = current_time.strftime("%Y.%M.%d")
            url_1 = "https://section.cafe.naver.com/ca-fe/home/search/articles?q=" + data[0]
            url_2 = url_1 + "&em=1&pr=7&ps=" + date_1[0] + "." + date_1[1] +"." + date_1[2]
            url_3 = url_2 + "&pe=" + time
            url_4 = url_3 + "&in=신고%20경고%20추방%20벤%20테러%20절도%20약탈%20욕설%20핵%20엑스레이%20매크로"
        
        webbrowser.open(url_4)
    
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

    def OK(self):
        str = self.listWidget.item(0).text()
        data = str.split(' - ')
        str = "환영합니다! " + data[0] + " 님!\n"
        str2 = """시작하기 전 규정 한번씩 읽고 접속하시길 바랍니다!
플레이에 필요한 모든정보는 위키를 찾아보시길 바랍니다.
규정 : https://cafe.naver.com/dellunatown/1499
위키 : https://www.notion.so/Delluna-Wiki-7708df010bc34d07912a2f23adbac918
자주묻는질문 : https://cafe.naver.com/dellunatown/1003
🌱델루나 초보자 가이드 : https://cafe.naver.com/dellunatown/12636
        """
        
        clipboard.copy(str + str2)

    def NO_PIC(self):
        str = self.listWidget.item(0).text()
        data = str.split(' - ')
        str = "사진 추가해주세요."
        clipboard.copy(str)

    def NO(self):
        str = self.listWidget.item(0).text()
        data = str.split(' - ')
        str = "타 서버 처벌기록으로 인해 가입 반려합니다."
        clipboard.copy(str)

    def WHITELIST(self):
        str = self.listWidget.item(0).text()
        data = str.split(' - ')
        str = "/whitelist add " + data[0]
        clipboard.copy(str)

    def getname(self):
        name = self.lineEdit.text().replace(' ', '')
        uuid = MojangAPI.get_uuid(name)
        self.lineEdit.clear()
        self.listWidget.clear()
        self.label_4.clear()
        if not uuid:
            self.listWidget.addItem("ERROR - Unkown User")
        else:
            profile = MojangAPI.get_profile(uuid)
            name_history_list = MojangAPI.get_name_history(uuid)
            name_history_list.reverse()

            response = requests.get("https://mc-heads.net/body/" + uuid + "/right.png")
            file = open("skin.png", "wb")
            file.write(response.content)
            file.close()
            self.label_4.setPixmap(QtGui.QPixmap("skin.png"))

            i = 1
            for data in name_history_list:
                timestamp = data['changed_to_at']
                if (timestamp == 0):
                    changetime = "2010-01-01"
                else:
                    changetime = datetime.date.fromtimestamp(timestamp/1000)
                self.listWidget.addItem(f"{data['name']} - {changetime}")
                
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = MainWindow() 
    myWindow.show()
    app.exec_()