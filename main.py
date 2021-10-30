import sys
from PyQt5.QtWidgets import *
from search_ui import Ui_MainWindow      #search_ui 是你的.py檔案名字
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5.QtWebEngineWidgets import QWebEnginePage
#from PyQt5.QtWebEngineWidgets import QWebEngineView
import threading
import urllib.request
import requests
from bs4 import BeautifulSoup
import numpy

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('肉搜神器')
        self.ui.pushButton.clicked.connect(self.Search_Student)
        self.ui.pushButton_2.clicked.connect(self.searchThread)
        self.ui.widget.load(QtCore.QUrl("https://www.mcu.edu.tw/student/new-query/sel-6-1.asp"))
        self.show()
    def searchThread(self):
        threadList=[]
        threadList.append(threading.Thread(target = self.classMemberSearch))
        threadList[-1].setDaemon(True)
        threadList[-1].start()
    
    def Search_Student(self):
        url = "https://www.mcu.edu.tw/student/%E6%A0%A1%E5%9C%92IC%E5%8D%A1%E7%85%A7%E7%89%87%E6%AA%94/student/"+self.ui.studentIdInput.text()+".jpg"    
        data = urllib.request.urlopen(url).read()
        studentImg = QPixmap()
        studentImg.loadFromData(data)
        studentImg_resize = studentImg.scaled(170, 232)
        self.ui.textLabel.setPixmap(studentImg_resize)
    def classMemberSearch(self):
        try:
            num=1
            print(str(self.ui.widget.url().url()))
            url = self.ui.widget.url().url()
            r = requests.get(url)       
            #print(r.status_code)
            soup = BeautifulSoup(r.text, "html.parser")
            studentList=[]
            for name in soup.find_all("td"):
                studentList.append(name.get_text())
                #print(name.get_text())
            for i in range(0,len(studentList),3):
                
                label = getattr(self.ui, 'label_{}'.format(num))
                label.setText('')
                url = "https://www.mcu.edu.tw/student/%E6%A0%A1%E5%9C%92IC%E5%8D%A1%E7%85%A7%E7%89%87%E6%AA%94/student/"+studentList[i]+".jpg"   
                print(label)
                data = urllib.request.urlopen(url).read()
                studentImg = QPixmap()
                studentImg.loadFromData(data)
                studentImg_resize = studentImg.scaled(150, 204)
                label.setPixmap(studentImg_resize)
                num += 1
                label = getattr(self.ui, 'label_{}'.format(num))
                label.setText('')
                label.setText(studentList[i]+'\n'+studentList[i+1])
                num += 1
                '''
                response = requests.get(urlID, stream=True)
                if(response.status_code==200):  
                    file_name = urlID.split('/')[-1]
                    file_name = file_name.split('.')[0]
                    file_name='./'+file_name+"_"+studentList[i]+".jpg"
                    with open(file_name, 'wb') as file:
                        shutil.copyfileobj(response.raw, file)
                    print(file_name)
                '''
        except:
            print('發生錯誤請重新嘗試')
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec_())