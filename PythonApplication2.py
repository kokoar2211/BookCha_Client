from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import socket
import login
import allRank
import SignUp
import bookCheck
import myReadBook
import recommend
import sys
from builtins import *
from PyQt4.Qt import *
import time
import recommend_rc

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(t):
        return t
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
      
class loginWindow(QMainWindow, login.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.showSignUp)
        self.pushButton.clicked.connect(self.showAllRank)
    def showAllRank(self):
        id = self.textEdit.text()
        password = self.textEdit_2.text()
        data = "LOGIN " +id +" " + password + '\n'
        s.send(data.encode())
        #버튼 클릭시 id password DB에서 비교, 맞으면 실행, 아니면 틀렸다 표시 출력
        data = s.recv(4096)
        data = data.decode()
        data = data.split()
        data = data[0]+data[1]+data[2]
        if(data == "LOGINOO"):
            self.close()
            showAllRankWin(id)
        elif(data == "LOGINOX"):
            self.warning.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600; color:#DB0000;\">비밀번호불일치</span></p></body></html>", None))
            #비밀번호 틀렸다고 표시 띄우기
        elif(data == "LOGINXX"):
            self.warning.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600; color:#DB0000;\">아이디불일치</span></p></body></html>", None))
            #아이디 틀렸다고 표시 띄우기'''
    def showSignUp(self):
         self.close()
         showSignUpWin()  
class SignUpWindow(QMainWindow, SignUp.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.showLogin)
        self.pushButton_2.clicked.connect(self.manCommand)
        self.pushButton.clicked.connect(self.womanCommand)
    def manCommand(self):
        self.gender = "남"
        self.pushButton_2.setFlat(False)
        self.pushButton.setFlat(True)
    def womanCommand(self):
        self.gender = "여"
        self.pushButton.setFlat(False)
        self.pushButton_2.setFlat(True)
    def showLogin(self):
        id = self.textEdit.text()
        password = self.textEdit_2.text()
        name = self.textEdit_3.text()
        if(password == self.textEdit_4.text()):
            birth = str(self.dateEdit.date().year()) + "-" + str(self.dateEdit.date().month())+ "-" + str(self.dateEdit.date().day())
        
            data = "REGISTER " +id + " " + password + " " + name + " " + birth + " " + self.gender + "\n"
            s.send(data.encode())
            data = s.recv(4096)
            data = data.decode()
            if(data == "REGISTER O\n"):
                self.close()
                showLoginWin()
            elif(data == "REGISTER X\n"):
                self.warning.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600; color:#DB0000;\">중복아이디존재</span></p></body></html>", None))
            elif(data == "REGISTER E\n"):
                self.warning.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600; color:#DB0000;\">BUG</span></p></body></html>", None))
            '''여기서 데이터들 서버로 넘기고 ID조회, 비밀번호 조회 화면 출력'''   
        else:
            self.warning.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600; color:#DB0000;\">패스워드불일치</span></p></body></html>", None))
class allRankWindow(QMainWindow, allRank.Ui_MainWindow):
    id = ""
    countMember = 0
    dataCheck = False
    count = 0
    BookList = []
    KoreanBookList = []
    isKorean = False
    EnglishBookList = []
    isEnglish = False
    JapanBookList = []
    isJapan = False
    ThrillerList = []
    RomanceList = []
    SFList = []
    FamilyList = []
    KoreanThrillerList = []
    KoreanRomanceList = []
    KoreanSFList = []
    KoreanFamilyList = []
    EnglishThrillerList = []
    EnglishRomanceList = []
    EnglishSFList = []
    EnglishFamilyList = []
    JapanThrillerList = []
    JapanRomanceList = []
    JapanSFList = []
    JapanFamilyList = []
    temp = []
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) 
        self.pushButton.clicked.connect(self.showAllRank)
        self.pushButton_2.clicked.connect(self.showRecommend)
        self.pushButton_3.clicked.connect(self.showBookCheck)
        self.pushButton_4.clicked.connect(self.showMyReadBook)
        self.verticalScrollBar.valueChanged.connect(self.moveList)
        self.AllNation.clicked.connect(self.showAllNationList)
        self.Korean.clicked.connect(self.showKoreanList)
        self.English.clicked.connect(self.showEnglishList)
        self.Japan.clicked.connect(self.showJapanList)
        self.AllGenre.clicked.connect(self.showAllGenre)
        self.Thriller.clicked.connect(self.showThriller)
        self.Romance.clicked.connect(self.showRomance)
        self.SF.clicked.connect(self.showSF)
        self.Family.clicked.connect(self.showFamily)
        self.Book1.clicked.connect(self.showBook1Info)
        self.Book2.clicked.connect(self.showBook2Info)
        self.Book3.clicked.connect(self.showBook3Info)
        self.Book4.clicked.connect(self.showBook4Info)
        self.Book5.clicked.connect(self.showBook5Info)
        self.Book6.clicked.connect(self.showBook6Info)
        self.Book7.clicked.connect(self.showBook7Info)
        self.Book8.clicked.connect(self.showBook8Info)
        self.Book9.clicked.connect(self.showBook9Info)
    def setInfo(self):
        if(self.dataCheck == False):
            self.clearData()
            self.dataCheck = True
            data = "COUNTMEMBER\n"
            s.send(data.encode())
            data = s.recv(4096)
            data = data.decode()
            data.split("\n")
            self.countMember = data[0]+data[1]
            self.setBookList()
            self.setImege(0,self.BookList)
            self.setScrollBar(self.BookList)            
            self.temp = self.BookList
    def setID(self,ID):
        self.id = ID 
        self.ID.setText(self.id)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("맑은 고딕"))
        self.ID.setFont(font)   
    def setScrollBar(self, List):
        if(len(List)<9):
            self.verticalScrollBar.setMaximum(1)
        else:
            self.verticalScrollBar.setMaximum(len(List)/9)
        self.verticalScrollBar.setValue(0)
    def setBookList(self):
        data = 'BOOKRANKALL ' + self.id +" \n"
        s.send(data.encode())
        count = 0;
        while(True):
            data = s.recv(4096)
            data = data.decode()
            data = data.split("\b")
            data.append(self.countMember)
            print(data)
            if(data[0] == 'end\n'):
                break
            self.BookList.append(Book(data))
            if(self.BookList[count].getBookNation() == "한국"):
                self.KoreanBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.KoreanThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.KoreanRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.KoreanSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.KoreanFamilyList.append(Book(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "영미"):
                self.EnglishBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.EnglishThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.EnglishRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.EnglishSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.EnglishFamilyList.append(Book(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "일본"):
                self.JapanBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.JapanThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.JapanRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.JapanSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.JapanFamilyList.append(Book(data))
                    count+=1
    def setImege(self, Scroolbar, List):
        buttonList = [ self.Book1, self.Book2, self.Book3, self.Book4, self.Book5, self.Book6, self.Book7, self.Book8, self.Book9 ]
        buttonNameList = [ self.Book1Name, self.Book2Name, self.Book3Name, self.Book4Name, self.Book5Name, self.Book6Name, self.Book7Name, self.Book8Name, self.Book9Name ]
        for i in range(0,9):
            if(len(List) > i+Scroolbar*9):
                buttonList[i].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+List[i+Scroolbar*9].getBookISBN()+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                buttonList[i].setIcon(icon)
                buttonList[i].setIconSize(QtCore.QSize(180, 180))
                buttonNameList[i].setText(List[i+Scroolbar*9].getBookName())
            else:
                buttonList[i].clearMask()
                buttonNameList[i].clearMask()
    def clearData(self):
        self.BookList.clear()
        self.KoreanBookList.clear()
        self.EnglishBookList.clear()
        self.JapanBookList.clear()
        self.ThrillerList.clear()
        self.RomanceList.clear()
        self.SFList.clear()
        self.FamilyList.clear()
        self.KoreanThrillerList.clear()
        self.KoreanRomanceList.clear()
        self.KoreanSFList.clear()
        self.KoreanFamilyList.clear()
        self.EnglishThrillerList.clear()
        self.EnglishRomanceList.clear()
        self.EnglishSFList.clear()
        self.EnglishFamilyList.clear()
        self.JapanThrillerList.clear()
        self.JapanRomanceList.clear()
        self.JapanSFList.clear()
        self.JapanFamilyList.clear()
    def moveList(self):
        self.setImege(self.verticalScrollBar.value(),self.temp)
    def showAllNationList(self):
        self.temp = self.BookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = False
    def showKoreanList(self):
        self.temp = self.KoreanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = True
        self.isEnglish = False
        self.isJapan = False
    def showEnglishList(self):
        self.temp = self.EnglishBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = True
        self.isJapan = False
    def showJapanList(self):
        self.temp = self.JapanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = True
    def showAllGenre(self):
        if(self.isKorean == True):
            self.temp = self.KoreanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.BookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showThriller(self):
        if(self.isKorean == True):
            self.temp = self.KoreanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.ThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showRomance(self):
        if(self.isKorean == True):
            self.temp = self.KoreanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.RomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showSF(self):
        if(self.isKorean == True):
            self.temp = self.KoreanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.SFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showFamily(self):
        if(self.isKorean == True):
            self.temp = self.KoreanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.FamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showBook1Info(self):
        data = "GETSUMMARY "+self.temp[0+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[0+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[0+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook2Info(self):
        data = "GETSUMMARY "+self.temp[1+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[1+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[1+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook3Info(self):
        data = "GETSUMMARY "+self.temp[2+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[2+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[2+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook4Info(self):
        data = "GETSUMMARY "+self.temp[3+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[3+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[3+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook5Info(self):
        data = "GETSUMMARY "+self.temp[4+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[4+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[4+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook6Info(self):
        data = "GETSUMMARY "+self.temp[5+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[5+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[5+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook7Info(self):
        data = "GETSUMMARY "+self.temp[6+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[6+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[6+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook8Info(self):
        data = "GETSUMMARY "+self.temp[7+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[7+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[7+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook9Info(self):
        data = "GETSUMMARY "+self.temp[8+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[8+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[8+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN_2.setText(temp[1])
        self.Author_2.setText(temp[2])
        self.Genre_2.setText(temp[3])
        self.Nation_2.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def getBookList(self,book,Korean,English,Japan,Thriller,Romance,SF,Family,KoreanThriller,KoreanRomance,KoreanSF,KoreanFamily,EnglishThriller,EnglishRomance,EnglishSF,EnglishFamily,JapanThriller,JapanRomance,JapanSF,JapanFamily):
        for i in self.BookList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            book.append(temp)
        for i in self.KoreanBookList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            Korean.append(i)
        for i in self.EnglishBookList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            English.append(i)
        for i in self.JapanBookList: 
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            Japan.append(i)
        for i in self.ThrillerList :
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            Thriller.append(i)
        for i in self.RomanceList: 
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            Romance.append(i)
        for i in self.SFList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            SF.append(i)
        for i in self.FamilyList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            Family.append(i)
        for i in self.KoreanThrillerList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            KoreanThriller.append(i)
        for i in self.KoreanRomanceList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            KoreanRomance.append(i)
        for i in self.KoreanSFList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            KoreanSF.append(i)
        for i in self.KoreanFamilyList :
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            KoreanFamily.append(i)
        for i in self.EnglishThrillerList :
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            EnglishThriller.append(i)
        for i in self.EnglishRomanceList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            EnglishRomance.append(i)
        for i in self.EnglishSFList :
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            EnglishSF.append(i)
        for i in self.EnglishFamilyList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            EnglishFamily.append(i)
        for i in self.JapanThrillerList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            JapanThriller.append(i)
        for i in self.JapanRomanceList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            JapanRomance.append(i)
        for i in self.JapanSFList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            JapanSF.append(i)
        for i in self.JapanFamilyList:
            temp = i.getBookInfoNotStory()
            temp.append(str(0))
            temp = CheckedBook(temp)
            JapanFamily.append(i)
    def showAllRank(self):
        self.close()
        showAllRankWin(self.id)
    def showBookCheck(self):
        self.close()
        showBookCheckWin(self.id)
    def showRecommend(self):
        self.close()
        showRecommendWin(self.id)
    def showMyReadBook(self):
        self.close()
        showMyReadBookWin(self.id)
class bookCheckWindow(QMainWindow, bookCheck.Ui_MainWindow):
    id = ""
    dataCheck = False
    count = 0
    BookList = []
    KoreanBookList = []
    isKorean = False
    EnglishBookList = []
    isEnglish = False
    JapanBookList = []
    isJapan = False
    ThrillerList = []
    RomanceList = []
    SFList = []
    FamilyList = []
    KoreanThrillerList = []
    KoreanRomanceList = []
    KoreanSFList = []
    KoreanFamilyList = []
    EnglishThrillerList = []
    EnglishRomanceList = []
    EnglishSFList = []
    EnglishFamilyList = []
    JapanThrillerList = []
    JapanRomanceList = []
    JapanSFList = []
    JapanFamilyList = []
    temp = []
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) 
        self.pushButton.clicked.connect(self.showAllRank)
        self.pushButton_2.clicked.connect(self.showRecommend)
        self.pushButton_3.clicked.connect(self.showBookCheck)
        self.pushButton_4.clicked.connect(self.showMyReadBook)
        self.verticalScrollBar.valueChanged.connect(self.moveList)
        self.AllNation.clicked.connect(self.showAllNationList)
        self.Korea.clicked.connect(self.showKoreanList)
        self.English.clicked.connect(self.showEnglishList)
        self.Japan.clicked.connect(self.showJapanList)
        self.AllGenre.clicked.connect(self.showAllGenre)
        self.Thriller.clicked.connect(self.showThriller)
        self.Romance.clicked.connect(self.showRomance)
        self.SF.clicked.connect(self.showSF)
        self.Family.clicked.connect(self.showFamily)
        self.Book1.clicked.connect(self.BookCheck1.click)
        self.Book2.clicked.connect(self.BookCheck2.click)
        self.Book3.clicked.connect(self.BookCheck3.click)
        self.Book4.clicked.connect(self.BookCheck4.click)
        self.Book5.clicked.connect(self.BookCheck5.click)
        self.Book6.clicked.connect(self.BookCheck6.click)
        self.Book7.clicked.connect(self.BookCheck7.click)
        self.Book8.clicked.connect(self.BookCheck8.click)
        self.Book9.clicked.connect(self.BookCheck9.click)
        self.Book10.clicked.connect(self.BookCheck10.click)
        self.Book11.clicked.connect(self.BookCheck11.click)
        self.Book12.clicked.connect(self.BookCheck12.click)
        self.Book13.clicked.connect(self.BookCheck13.click)
        self.Book14.clicked.connect(self.BookCheck14.click)
        self.Book15.clicked.connect(self.BookCheck15.click)
        self.Book16.clicked.connect(self.BookCheck16.click)
        self.Book17.clicked.connect(self.BookCheck17.click)
        self.Book18.clicked.connect(self.BookCheck18.click)
        self.BookCheck1.clicked.connect(self.clickedBook1)
        self.BookCheck2.clicked.connect(self.clickedBook2)
        self.BookCheck3.clicked.connect(self.clickedBook3)
        self.BookCheck4.clicked.connect(self.clickedBook4)
        self.BookCheck5.clicked.connect(self.clickedBook5)
        self.BookCheck6.clicked.connect(self.clickedBook6)
        self.BookCheck7.clicked.connect(self.clickedBook7)
        self.BookCheck8.clicked.connect(self.clickedBook8)
        self.BookCheck9.clicked.connect(self.clickedBook9)
        self.BookCheck10.clicked.connect(self.clickedBook10)
        self.BookCheck11.clicked.connect(self.clickedBook11)
        self.BookCheck12.clicked.connect(self.clickedBook12)
        self.BookCheck13.clicked.connect(self.clickedBook13)
        self.BookCheck14.clicked.connect(self.clickedBook14)
        self.BookCheck15.clicked.connect(self.clickedBook15)
        self.BookCheck16.clicked.connect(self.clickedBook16)
        self.BookCheck17.clicked.connect(self.clickedBook17)
        self.BookCheck18.clicked.connect(self.clickedBook18)
    def setInfo(self,ID):
        if(self.dataCheck == False):
            self.clearData()
            self.id = ID 
            self.dataCheck = True
            self.ID.setText(self.id)
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("맑은 고딕"))
            self.ID.setFont(font)
            data = "COUNTMEMBER\n"
            s.send(data.encode())
            data = s.recv(4096)
            data = data.decode()
            data.split("\n")
            print(data)
            self.countMember = data[0] + data[1]
            self.setBookList()
            self.setImege(0,self.BookList)
            self.setScrollBar(self.BookList)            
            self.temp = self.BookList
        elif(self.dataCheck == True):
            self.id = ID 
            self.ID.setText(self.id)
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("맑은 고딕"))
            self.ID.setFont(font)
            data = "COUNTMEMBER\n"
            s.send(data.encode())
            data = s.recv(4096)
            data = data.decode()
            data.split("\n")
            self.countMember = data[0]+data[1]
            self.setImege(0,self.BookList)
            self.setScrollBar(self.BookList)            
            self.temp = self.BookList
    def setScrollBar(self, List):
        if(len(List)<18):
            self.verticalScrollBar.setMaximum(1)
        else:
            self.verticalScrollBar.setMaximum(len(List)/18)
        self.verticalScrollBar.setValue(0)
    def setBookList(self):
        data = 'BOOKCHECKALL ' + self.id +" \n"
        s.send(data.encode())
        count = 0;
        while(True):
            data = s.recv(4096)
            data = data.decode()
            data = data.split("\b")
            data.append(self.countMember)
            print(data)
            if(data[0] == 'end\n'):
                break
            self.BookList.append(CheckedBook(data))
            if(self.BookList[count].getBookNation() == "한국"):
                self.KoreanBookList.append(CheckedBook(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(CheckedBook(data))
                    self.KoreanThrillerList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(CheckedBook(data))
                    self.KoreanRomanceList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(CheckedBook(data))
                    self.KoreanSFList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(CheckedBook(data))
                    self.KoreanFamilyList.append(CheckedBook(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "영미"):
                self.EnglishBookList.append(CheckedBook(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(CheckedBook(data))
                    self.EnglishThrillerList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(CheckedBook(data))
                    self.EnglishRomanceList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(CheckedBook(data))
                    self.EnglishSFList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(CheckedBook(data))
                    self.EnglishFamilyList.append(CheckedBook(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "일본"):
                self.JapanBookList.append(CheckedBook(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(CheckedBook(data))
                    self.JapanThrillerList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(CheckedBook(data))
                    self.JapanRomanceList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(CheckedBook(data))
                    self.JapanSFList.append(CheckedBook(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(CheckedBook(data))
                    self.JapanFamilyList.append(CheckedBook(data))
                    count+=1
    def setImege(self, Scroolbar, List):
        buttonList = [ self.Book1, self.Book2, self.Book3, self.Book4, self.Book5, self.Book6, self.Book7, self.Book8, self.Book9, self.Book10, self.Book11, self.Book12, self.Book13, self.Book14, self.Book15, self.Book16, self.Book17, self.Book18]
        buttonNameList = [ self.BookCheck1, self.BookCheck2, self.BookCheck3, self.BookCheck4, self.BookCheck5, self.BookCheck6, self.BookCheck7, self.BookCheck8, self.BookCheck9, self.BookCheck10, self.BookCheck11, self.BookCheck12, self.BookCheck13, self.BookCheck14, self.BookCheck15, self.BookCheck16, self.BookCheck17, self.BookCheck18]
        for i in range(0,18):
            if(len(List) > i+Scroolbar*18):
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+List[i+Scroolbar*18].getBookISBN()+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                buttonList[i].setIcon(icon)
                buttonList[i].setIconSize(QtCore.QSize(180, 180))
                buttonNameList[i].setText(List[i+Scroolbar*18].getBookName())
                for j in self.BookList:
                    if(List[i+Scroolbar*18].getBookName() == j.getBookName()):
                        buttonNameList[i].setChecked(j.getBookCheck())
                        break
            else:
                buttonList[i].destroy()
                buttonNameList[i].destroy()
    def moveList(self):
        self.setImege(self.verticalScrollBar.value(),self.temp)        
    def clearData(self):
        self.BookList.clear()
        self.KoreanBookList.clear()
        self.EnglishBookList.clear()
        self.JapanBookList.clear()
        self.ThrillerList.clear()
        self.RomanceList.clear()
        self.SFList.clear()
        self.FamilyList.clear()
        self.KoreanThrillerList.clear()
        self.KoreanRomanceList.clear()
        self.KoreanSFList.clear()
        self.KoreanFamilyList.clear()
        self.EnglishThrillerList.clear()
        self.EnglishRomanceList.clear()
        self.EnglishSFList.clear()
        self.EnglishFamilyList.clear()
        self.JapanThrillerList.clear()
        self.JapanRomanceList.clear()
        self.JapanSFList.clear()
        self.JapanFamilyList.clear()       
    def showAllNationList(self):
        self.temp = self.BookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = False
    def showKoreanList(self):
        self.temp = self.KoreanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = True
        self.isEnglish = False
        self.isJapan = False
    def showEnglishList(self):
        self.temp = self.EnglishBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = True
        self.isJapan = False
    def showJapanList(self):
        self.temp = self.JapanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = True
    def showAllGenre(self):
        if(self.isKorean == True):
            self.temp = self.KoreanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.BookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showThriller(self):
        if(self.isKorean == True):
            self.temp = self.KoreanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.ThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showRomance(self):
        if(self.isKorean == True):
            self.temp = self.KoreanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.RomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showSF(self):
        if(self.isKorean == True):
            self.temp = self.KoreanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.SFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showFamily(self):
        if(self.isKorean == True):
            self.temp = self.KoreanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.FamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def clickedBook1(self):
        if(self.BookCheck1.isChecked() == True):
            temp = self.temp[0 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck1.isChecked() == False):
            temp = self.temp[0 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)    
                    break
    def clickedBook2(self):
        if(self.BookCheck2.isChecked() == True):
            temp = self.temp[1 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck2.isChecked() == False):
            temp = self.temp[1 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook3(self):
        if(self.BookCheck3.isChecked() == True):
            temp = self.temp[2 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck3.isChecked() == False):
            temp = self.temp[2 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook4(self):
        if(self.BookCheck4.isChecked() == True):
            temp = self.temp[3 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck4.isChecked() == False):
            temp = self.temp[3 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook5(self):
        if(self.BookCheck5.isChecked() == True):
            temp = self.temp[4 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck5.isChecked() == False):
            temp = self.temp[4 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook6(self):
        if(self.BookCheck6.isChecked() == True):
            temp = self.temp[5 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck6.isChecked() == False):
            temp = self.temp[5 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook7(self):
        if(self.BookCheck7.isChecked() == True):
            temp = self.temp[6 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck7.isChecked() == False):
            temp = self.temp[6 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook8(self):
        if(self.BookCheck8.isChecked() == True):
            temp = self.temp[7 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck8.isChecked() == False):
            temp = self.temp[7 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook9(self):
        if(self.BookCheck9.isChecked() == True):
            temp = self.temp[8 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck9.isChecked() == False):
            temp = self.temp[8 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook10(self):
        if(self.BookCheck10.isChecked() == True):
            temp = self.temp[9 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck10.isChecked() == False):
            temp = self.temp[9 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook11(self):
        if(self.BookCheck11.isChecked() == True):
            temp = self.temp[10 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck11.isChecked() == False):
            temp = self.temp[10 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook12(self):
        if(self.BookCheck12.isChecked() == True):
            temp = self.temp[11 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck12.isChecked() == False):
            temp = self.temp[11 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook13(self):
        if(self.BookCheck13.isChecked() == True):
            temp = self.temp[12 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck13.isChecked() == False):
            temp = self.temp[12 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook14(self):
        if(self.BookCheck14.isChecked() == True):
            temp = self.temp[13 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck14.isChecked() == False):
            temp = self.temp[13 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook15(self):
        if(self.BookCheck15.isChecked() == True):
            temp = self.temp[14 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck15.isChecked() == False):
            temp = self.temp[14 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook16(self):
        if(self.BookCheck16.isChecked() == True):
            temp = self.temp[15 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck16.isChecked() == False):
            temp = self.temp[15 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook17(self):
        if(self.BookCheck17.isChecked() == True):
            temp = self.temp[16 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck17.isChecked() == False):
            temp = self.temp[16 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def clickedBook18(self):
        if(self.BookCheck18.isChecked() == True):
            temp = self.temp[17 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(True)
                    break
        elif(self.BookCheck18.isChecked() == False):
            temp = self.temp[17 + self.verticalScrollBar.value() * 18].getBookName()
            for i in self.BookList :
                if(i.getBookName() == temp):
                    i.setChecked(False)
                    break
    def showAllRank(self):
        self.close()
        self.saveCheckedBook()
        showAllRankWin(self.id)    
    def showBookCheck(self):
        self.saveCheckedBook()
        self.close()
        showBookCheckWin(self.id)
    def showRecommend(self):
        self.close()
        self.saveCheckedBook()
        showRecommendWin(self.id)
    def showMyReadBook(self):
        self.close()
        self.saveCheckedBook()
        showMyReadBookWin(self.id)
    def saveCheckedBook(self):
        isTemp = True;
        temp = []
        for i in range(0,len(self.BookList)) :
            if(self.BookList[i].getBookCheck() == True):
                data = "READ "+ self.id +" "+self.BookList[i].getBookISBN() + "\n"
                temp.append(self.BookList[i])
                s.send(data.encode())
                if(isTemp == True):
                    self.dataCheck = False
                    cheakedFalse()
                    isTemp = False
                time.sleep(0.1)
        checkdelete(temp)                                
class recommendWindow(QMainWindow, recommend.Ui_MainWindow):
    id = ""
    countMember = 0
    dataCheck = False
    count = 0
    BookList = []
    KoreanBookList = []
    isKorean = False
    EnglishBookList = []
    isEnglish = False
    JapanBookList = []
    isJapan = False
    ThrillerList = []
    RomanceList = []
    SFList = []
    FamilyList = []
    KoreanThrillerList = []
    KoreanRomanceList = []
    KoreanSFList = []
    KoreanFamilyList = []
    EnglishThrillerList = []
    EnglishRomanceList = []
    EnglishSFList = []
    EnglishFamilyList = []
    JapanThrillerList = []
    JapanRomanceList = []
    JapanSFList = []
    JapanFamilyList = []
    temp = []   
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) 
        self.pushButton.clicked.connect(self.showAllRank)
        self.pushButton_2.clicked.connect(self.showRecommend)
        self.pushButton_3.clicked.connect(self.showBookCheck)
        self.pushButton_4.clicked.connect(self.showMyReadBook)
        self.verticalScrollBar.valueChanged.connect(self.moveList)
        self.AllNation.clicked.connect(self.showAllNationList)
        self.Korea.clicked.connect(self.showKoreanList)
        self.English.clicked.connect(self.showEnglishList)
        self.Japan.clicked.connect(self.showJapanList)
        self.AllGenre.clicked.connect(self.showAllGenre)
        self.Thriller.clicked.connect(self.showThriller)
        self.Romance.clicked.connect(self.showRomance)
        self.SF.clicked.connect(self.showSF)
        self.Family.clicked.connect(self.showFamily)
        self.Book1.clicked.connect(self.showBook1Info)
        self.Book2.clicked.connect(self.showBook2Info)
        self.Book3.clicked.connect(self.showBook3Info)
        self.Book4.clicked.connect(self.showBook4Info)
        self.Book5.clicked.connect(self.showBook5Info)
        self.Book6.clicked.connect(self.showBook6Info)
        self.Book7.clicked.connect(self.showBook7Info)
        self.Book8.clicked.connect(self.showBook8Info)
        self.Book9.clicked.connect(self.showBook9Info)
    def setInfo(self,ID):
        if(self.dataCheck == False):
            self.clearData()
            self.id = ID 
            self.dataCheck = True
            self.ID.setText(self.id)
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("맑은 고딕"))
            self.ID.setFont(font)
            data = "COUNTMEMBER\n"
            s.send(data.encode())
            data = s.recv(4096)
            data = data.decode()
            data.split("\n")
            self.countMember = data[0] + data[1]
            self.setBookList()
            self.setImege(0,self.BookList)
            self.setScrollBar(self.BookList)            
            self.temp = self.BookList
    def setScrollBar(self, List):
        if(len(List)<9):
            self.verticalScrollBar.setMaximum(1)
        else:
            self.verticalScrollBar.setMaximum(len(List)/9)
        self.verticalScrollBar.setValue(0)
    def setBookList(self):
        data = 'EACHRANKALL ' + self.id +" \n"
        s.send(data.encode())
        count = 0;
        while(True):
            data = s.recv(4096)
            data = data.decode()
            data = data.split("\b")
            data.append(self.countMember)
            print(data)
            if(data[0] == 'end\n'):
                break
            self.BookList.append(Book(data))
            if(self.BookList[count].getBookNation() == "한국"):
                self.KoreanBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.KoreanThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.KoreanRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.KoreanSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.KoreanFamilyList.append(Book(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "영미"):
                self.EnglishBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.EnglishThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.EnglishRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.EnglishSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.EnglishFamilyList.append(Book(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "일본"):
                self.JapanBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.JapanThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.JapanRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.JapanSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.JapanFamilyList.append(Book(data))
                    count+=1
    def setImege(self, Scroolbar, List):
        buttonList = [ self.Book1, self.Book2, self.Book3, self.Book4, self.Book5, self.Book6, self.Book7, self.Book8, self.Book9 ]
        buttonNameList = [ self.Book1Name, self.Book2Name, self.Book3Name, self.Book4Name, self.Book5Name, self.Book6Name, self.Book7Name, self.Book8Name, self.Book9Name ]
        for i in range(0,9):
            if(len(List) > i+Scroolbar*9):
                buttonList[i].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+List[i+Scroolbar*9].getBookISBN()+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                buttonList[i].setIcon(icon)
                buttonList[i].setIconSize(QtCore.QSize(180, 180))
                buttonNameList[i].setText(List[i+Scroolbar*9].getBookName())
            else:
                buttonList[i].clearMask()
                buttonNameList[i].clearMask()
    def clearData(self):
        self.BookList.clear()
        self.KoreanBookList.clear()
        self.EnglishBookList.clear()
        self.JapanBookList.clear()
        self.ThrillerList.clear()
        self.RomanceList.clear()
        self.SFList.clear()
        self.FamilyList.clear()
        self.KoreanThrillerList.clear()
        self.KoreanRomanceList.clear()
        self.KoreanSFList.clear()
        self.KoreanFamilyList.clear()
        self.EnglishThrillerList.clear()
        self.EnglishRomanceList.clear()
        self.EnglishSFList.clear()
        self.EnglishFamilyList.clear()
        self.JapanThrillerList.clear()
        self.JapanRomanceList.clear()
        self.JapanSFList.clear()
        self.JapanFamilyList.clear()
    def moveList(self):
        self.setImege(self.verticalScrollBar.value(),self.temp)
    def showAllNationList(self):
        self.temp = self.BookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = False
    def showKoreanList(self):
        self.temp = self.KoreanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = True
        self.isEnglish = False
        self.isJapan = False
    def showEnglishList(self):
        self.temp = self.EnglishBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = True
        self.isJapan = False
    def showJapanList(self):
        self.temp = self.JapanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = True
    def showAllGenre(self):
        if(self.isKorean == True):
            self.temp = self.KoreanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.BookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showThriller(self):
        if(self.isKorean == True):
            self.temp = self.KoreanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.ThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showRomance(self):
        if(self.isKorean == True):
            self.temp = self.KoreanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.RomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showSF(self):
        if(self.isKorean == True):
            self.temp = self.KoreanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.SFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showFamily(self):
        if(self.isKorean == True):
            self.temp = self.KoreanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.FamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showBook1Info(self):
        data = "GETSUMMARY "+self.temp[0+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[0+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[0+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook2Info(self):
        data = "GETSUMMARY "+self.temp[1+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[1+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[1+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook3Info(self):
        data = "GETSUMMARY "+self.temp[2+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[2+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[2+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook4Info(self):
        data = "GETSUMMARY "+self.temp[3+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[3+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[3+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook5Info(self):
        data = "GETSUMMARY "+self.temp[4+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[4+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[4+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook6Info(self):
        data = "GETSUMMARY "+self.temp[5+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[5+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[5+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook7Info(self):
        data = "GETSUMMARY "+self.temp[6+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[6+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[6+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook8Info(self):
        data = "GETSUMMARY "+self.temp[7+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[7+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[7+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook9Info(self):
        data = "GETSUMMARY "+self.temp[8+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[8+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[8+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")        
    def showAllRank(self):
        self.close()
        showAllRankWin(self.id)
    def showBookCheck(self):
        self.close()
        showBookCheckWin(self.id)
    def showRecommend(self):
        self.close()
        showRecommendWin(self.id)
    def showMyReadBook(self):
        self.close()
        showMyReadBookWin(self.id)
class myReadBookWindow(QMainWindow, myReadBook.Ui_MainWindow):
    id = ""
    countMember = 0
    dataCheck = False
    count = 0
    BookList = []
    KoreanBookList = []
    isKorean = False
    EnglishBookList = []
    isEnglish = False
    JapanBookList = []
    isJapan = False
    ThrillerList = []
    RomanceList = []
    SFList = []
    FamilyList = []
    KoreanThrillerList = []
    KoreanRomanceList = []
    KoreanSFList = []
    KoreanFamilyList = []
    EnglishThrillerList = []
    EnglishRomanceList = []
    EnglishSFList = []
    EnglishFamilyList = []
    JapanThrillerList = []
    JapanRomanceList = []
    JapanSFList = []
    JapanFamilyList = []
    temp = []
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) 
        self.pushButton.clicked.connect(self.showAllRank)
        self.pushButton_2.clicked.connect(self.showRecommend)
        self.pushButton_3.clicked.connect(self.showBookCheck)
        self.pushButton_4.clicked.connect(self.showMyReadBook)
        self.verticalScrollBar.valueChanged.connect(self.moveList)
        self.AllNation.clicked.connect(self.showAllNationList)
        self.Korean.clicked.connect(self.showKoreanList)
        self.English.clicked.connect(self.showEnglishList)
        self.Japan.clicked.connect(self.showJapanList)
        self.AllGenre.clicked.connect(self.showAllGenre)
        self.Thriller.clicked.connect(self.showThriller)
        self.Romance.clicked.connect(self.showRomance)
        self.SF.clicked.connect(self.showSF)
        self.Family.clicked.connect(self.showFamily)
        self.Book1.clicked.connect(self.showBook1Info)
        self.Book2.clicked.connect(self.showBook2Info)
        self.Book3.clicked.connect(self.showBook3Info)
        self.Book4.clicked.connect(self.showBook4Info)
        self.Book5.clicked.connect(self.showBook5Info)
        self.Book6.clicked.connect(self.showBook6Info)
        self.Book7.clicked.connect(self.showBook7Info)
        self.Book8.clicked.connect(self.showBook8Info)
        self.Book9.clicked.connect(self.showBook9Info)
    def setInfo(self,ID):
        if(self.dataCheck == False):
            self.clearData()
            self.id = ID 
            self.dataCheck = True
            self.ID.setText(self.id)
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("맑은 고딕"))
            self.ID.setFont(font)
            data = "COUNTMEMBER\n"
            s.send(data.encode())
            data = s.recv(4096)
            data = data.decode()
            data.split("\n")
            self.countMember = data[0] + data[1]
            self.setBookList()
            self.setImege(0,self.BookList)
            self.setScrollBar(self.BookList)            
            self.temp = self.BookList
            self.setRecommendCount()
    def clearData(self):
        self.BookList.clear()
        self.KoreanBookList.clear()
        self.EnglishBookList.clear()
        self.JapanBookList.clear()
        self.ThrillerList.clear()
        self.RomanceList.clear()
        self.SFList.clear()
        self.FamilyList.clear()
        self.KoreanThrillerList.clear()
        self.KoreanRomanceList.clear()
        self.KoreanSFList.clear()
        self.KoreanFamilyList.clear()
        self.EnglishThrillerList.clear()
        self.EnglishRomanceList.clear()
        self.EnglishSFList.clear()
        self.EnglishFamilyList.clear()
        self.JapanThrillerList.clear()
        self.JapanRomanceList.clear()
        self.JapanSFList.clear()
        self.JapanFamilyList.clear()
    def setScrollBar(self, List):
        if(len(List)<9):
            self.verticalScrollBar.setMaximum(1)
        else:
            self.verticalScrollBar.setMaximum(len(List)/9)
        self.verticalScrollBar.setValue(0)
    def setRecommendCount(self):
        self.KoreanReadingCount.setText(str(len(self.BookList)))
        self.EnglishRedingCount.setText(str(len(self.KoreanBookList)))
        self.JapanRedingCount.setText(str(len(self.JapanBookList)))
        self.ChinaRedingCount.setText(str(len(self.EnglishBookList)))
        self.franceReadingCount.setText(str(len(self.BookList)))
        self.HistoryRedingCount.setText(str(len(self.ThrillerList)))
        self.ThrillerRedingCount.setText(str(len(self.RomanceList)))
        self.RomanceReadingCount.setText(str(len(self.SFList)))
        self.SFReadingCount.setText(str(len(self.FamilyList)))
    def setBookList(self):
        data = 'MYREADBOOK ' + self.id +" \n"
        s.send(data.encode())
        count = 0;
        while(True):
            data = s.recv(4096)
            data = data.decode()
            data = data.split("\b")
            data.append(self.countMember)
            print(data)
            if(data[0] == 'end\n'):
                break
            self.BookList.append(Book(data))
            if(self.BookList[count].getBookNation() == "한국"):
                self.KoreanBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.KoreanThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.KoreanRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.KoreanSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.KoreanFamilyList.append(Book(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "영미"):
                self.EnglishBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.EnglishThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.EnglishRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.EnglishSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.EnglishFamilyList.append(Book(data))
                    count+=1
            elif(self.BookList[count].getBookNation() == "일본"):
                self.JapanBookList.append(Book(data))
                if(self.BookList[count].getBookGenre() == "공포_스릴러"):
                    self.ThrillerList.append(Book(data))
                    self.JapanThrillerList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "로맨스"):
                    self.RomanceList.append(Book(data))
                    self.JapanRomanceList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "SF_과학"):
                    self.SFList.append(Book(data))
                    self.JapanSFList.append(Book(data))
                    count+=1
                elif(self.BookList[count].getBookGenre() == "가족_성장"):
                    self.FamilyList.append(Book(data))
                    self.JapanFamilyList.append(Book(data))
                    count+=1
    def setImege(self, Scroolbar, List):
        buttonList = [ self.Book1, self.Book2, self.Book3, self.Book4, self.Book5, self.Book6, self.Book7, self.Book8, self.Book9 ]
        buttonNameList = [ self.Book1Name, self.Book2Name, self.Book3Name, self.Book4Name, self.Book5Name, self.Book6Name, self.Book7Name, self.Book8Name, self.Book9Name ]
        for i in range(0,9):
            if(len(List) > i+Scroolbar*9):
                buttonList[i].setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+List[i+Scroolbar*9].getBookISBN()+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                buttonList[i].setIcon(icon)
                buttonList[i].setIconSize(QtCore.QSize(180, 180))
                buttonNameList[i].setText(List[i+Scroolbar*9].getBookName())
            else:
                buttonList[i].clearMask()
                buttonNameList[i].clearMask()
    def moveList(self):
        self.setImege(self.verticalScrollBar.value(),self.temp)
    def showAllNationList(self):
        self.temp = self.BookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = False
    def showKoreanList(self):
        self.temp = self.KoreanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = True
        self.isEnglish = False
        self.isJapan = False
    def showEnglishList(self):
        self.temp = self.EnglishBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = True
        self.isJapan = False
    def showJapanList(self):
        self.temp = self.JapanBookList
        self.setScrollBar(self.temp)
        self.setImege(0,self.temp)
        self.isKorean = False
        self.isEnglish = False
        self.isJapan = True
    def showAllGenre(self):
        if(self.isKorean == True):
            self.temp = self.KoreanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanBookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.BookList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showThriller(self):
        if(self.isKorean == True):
            self.temp = self.KoreanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.ThrillerList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showRomance(self):
        if(self.isKorean == True):
            self.temp = self.KoreanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanRomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.RomanceList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showSF(self):
        if(self.isKorean == True):
            self.temp = self.KoreanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanSFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.SFList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showFamily(self):
        if(self.isKorean == True):
            self.temp = self.KoreanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isEnglish == True):
            self.temp = self.EnglishFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        elif(self.isJapan == True):
            self.temp = self.JapanFamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
        else:
            self.temp = self.FamilyList
            self.setScrollBar(self.temp)
            self.setImege(0,self.temp)
    def showBook1Info(self):
        data = "GETSUMMARY "+self.temp[0+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[0+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[0+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook2Info(self):
        data = "GETSUMMARY "+self.temp[1+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[1+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[1+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook3Info(self):
        data = "GETSUMMARY "+self.temp[2+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[2+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[2+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook4Info(self):
        data = "GETSUMMARY "+self.temp[3+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[3+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[3+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook5Info(self):
        data = "GETSUMMARY "+self.temp[4+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[4+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[4+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook6Info(self):
        data = "GETSUMMARY "+self.temp[5+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[5+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[5+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook7Info(self):
        data = "GETSUMMARY "+self.temp[6+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[6+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[6+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook8Info(self):
        data = "GETSUMMARY "+self.temp[7+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[7+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[7+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showBook9Info(self):
        data = "GETSUMMARY "+self.temp[8+self.verticalScrollBar.value()*9].getBookISBN()+"\n"
        s.send(data.encode())
        data =s.recv(4096)
        self.temp[8+self.verticalScrollBar.value()*9].setBookStory(data.decode())
        temp = self.temp[8+self.verticalScrollBar.value()*9].getBookInfo()
        self.BookName.setText(temp[0])
        self.ISBN.setText(temp[1])
        self.Author.setText(temp[2])
        self.Genre.setText(temp[3])
        self.Nation.setText(temp[4])
        self.RecommendCount.setText(temp[5])
        self.BookInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">"+temp[6]+"</span></p></body></html>", None))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Book/"+temp[1]+".jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainBook.setIcon(icon)
        self.mainBook.setIconSize(QtCore.QSize(180, 180))
        self.mainBook.setText("")
    def showAllRank(self):
        self.close()
        showAllRankWin(self.id)
    def showBookCheck(self):
        self.close()
        showBookCheckWin(self.id)
    def showRecommend(self):
        self.close()
        showRecommendWin(self.id)
    def showMyReadBook(self):
        self.close()
        showMyReadBookWin(self.id)
class Book(object):
    name = ""
    ISBN = 0
    author = ""
    genre = ""
    nation = ""
    story = ""
    recommendCount = 0
    def __init__(self,BookInfo):
        if(len(BookInfo) == 7):
            self.name = BookInfo[0]
            self.ISBN = BookInfo[1]
            self.author = BookInfo[2]
            self.genre = BookInfo[3]
            self.nation = BookInfo[4]
        #self.story = BookInfo[4]
            self.recommendCount = BookInfo[5]
            self.recommendCount = self.recommendCount.split("\n")
            self.recommendCount = self.recommendCount[0] + " / " + BookInfo[6]
        else :
            self.name = BookInfo[0]
            self.ISBN = BookInfo[1]
            self.genre = BookInfo[2]
            self.nation = BookInfo[3]
            self.recommendCount = BookInfo[4]
        
    def setBookStory(self,stroy):
        self.stroy = stroy
    def getBookInfo(self):
        result = [ self.name, self.ISBN, self.author, self.genre, self.nation, self.recommendCount,self.stroy ]
        return result
    def getBookInfoNotStory(self):
        result = [ self.name, self.ISBN, self.author, self.genre, self.nation, self.recommendCount]
        return result
    def getBookName(self):
        return self.name
    def getBookGenre(self):
        return self.genre
    def getBookNation(self):
        return self.nation
    def getBookISBN(self):
        return self.ISBN
class CheckedBook(Book):
    isChecked = False
    def __init__(self, BookInfo):
        Book.__init__(self,BookInfo)
        self.isChecked = False
    def setChecked(self,Check):
        self.isChecked = Check
    def getBookCheck(self):
        return self.isChecked
class thread(QThread):    
    def __init__(self,parent=None):
        super(thread,self).__init__(parent)
    def run(self):
        self.emit(SIGNAL("Windows()"))
class LodingWindow(QMainWindow):
    def __init__(self, parent=None):
        super(LodingWindow, self).__init__(parent)
        self.thread = thread()
        self.status_txt = QtGui.QLabel()
        self.movie = QtGui.QMovie(_fromUtf8(":/UI/loading4.gif"))
        self.movie.start()
        self.status_txt.setMovie(self.movie)
        self.status_txt.setWindowFlags(QtCore.Qt.CustomizeWindowHint) or self.status_txt.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.connect(self.thread, SIGNAL("Windows()"), self.showWindow)
    def showWindow(self):
        self.status_txt.show()
    def showWin(self):
        self.thread.start()
    def closeThread(self):
        self.thread.quit()
app = QApplication(sys.argv)
logWin = loginWindow()
SignUpWin = SignUpWindow()
allRankWin = allRankWindow()
bookCheckWin = bookCheckWindow()
myReadBookWin = myReadBookWindow()
recommendWin = recommendWindow()
loding = LodingWindow()
host = "52.78.101.189" #'202.31.130.93' #'25.53.26.214' #
port = 8888 #9999 #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
loding.showWin()
allRankWin.setInfo()
loding.close()   
logWin.show()
def cheakedFalse():
    myReadBookWin.dataCheck = False
    recommendWin.dataCheck = False
def showLoginWin():
    logWin.show()
def showSignUpWin():
    SignUpWin.show()
def showBookCheckWin(id):
    status_txt = QtGui.QLabel()
    movie = QtGui.QMovie(_fromUtf8(":/UI/loading4.gif"))
    movie.start()
    status_txt.setMovie(movie)
    status_txt.setWindowFlags(QtCore.Qt.CustomizeWindowHint) or status_txt.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    status_txt.show()
    if(bookCheckWin.dataCheck == False):
        book = []
        Korean = []
        English = []
        Japan = []
        Thriller = []
        Romance = []
        SF = []
        Family = []
        KoreanThriller = []
        KoreanRomance = []
        KoreanSF = []
        KoreanFamily = []
        EnglishThriller = []
        EnglishRomance = []
        EnglishSF = []
        EnglishFamily = []
        JapanThriller = []
        JapanRomance = []
        JapanSF = []
        JapanFamily = []
        allRankWin.getBookList(book,Korean,English,Japan,Thriller,Romance,SF,Family,KoreanThriller,KoreanRomance,KoreanSF,KoreanFamily,EnglishThriller,EnglishRomance,EnglishSF,EnglishFamily,JapanThriller,JapanRomance,JapanSF,JapanFamily)
        bookCheckWin.BookList = book
        bookCheckWin.KoreanBookList = Korean
        bookCheckWin.EnglishBookList = English
        bookCheckWin.JapanBookList = Japan
        bookCheckWin.ThrillerList = Thriller
        bookCheckWin.RomanceList = Romance
        bookCheckWin.SFList = SF
        bookCheckWin.FamilyList = Family
        bookCheckWin.KoreanThrillerList = KoreanThriller
        bookCheckWin.KoreanRomanceList = KoreanRomance
        bookCheckWin.KoreanSFList = KoreanSF
        bookCheckWin.KoreanFamilyList = KoreanFamily
        bookCheckWin.EnglishThrillerList = EnglishThriller
        bookCheckWin.EnglishRomanceList = EnglishRomance
        bookCheckWin.EnglishSFList = EnglishSF
        bookCheckWin.EnglishFamilyList = EnglishFamily
        bookCheckWin.JapanThrillerList = JapanThriller
        bookCheckWin.JapanRomanceList = JapanRomance
        bookCheckWin.JapanSFList = JapanSF
        bookCheckWin.JapanFamilyList = JapanFamily
        data = 'MYREADBOOK ' + id +" \n"
        s.send(data.encode())
        temp = []
        while(True):
            data = s.recv(4096)
            data = data.decode()
            if(data == "end\n"):
                break 
            data = data.split("\b")
            data.append("0")
            temp.append(Book(data))
            print(data)
        checkdelete(temp)   
        bookCheckWin.dataCheck = True
    bookCheckWin.setInfo(id)
    status_txt.close()
    bookCheckWin.show()
def checkdelete(temp):
    for j in temp:
        data = j.getBookName()
        for i in range(0,len(bookCheckWin.BookList)):
            if(data == bookCheckWin.BookList[i].getBookName()):
                del bookCheckWin.BookList[i]
                break
        for i in range(0,len(bookCheckWin.KoreanBookList)):
            if(data == bookCheckWin.KoreanBookList[i].getBookName()):
                del bookCheckWin.KoreanBookList[i]
                break
        for i in range(0,len(bookCheckWin.EnglishBookList)):
            if(data == bookCheckWin.EnglishBookList[i].getBookName()):
                del bookCheckWin.EnglishBookList[i]
                break
        for i in range(0,len(bookCheckWin.JapanBookList)):
            if(data == bookCheckWin.JapanBookList[i].getBookName()):
                del bookCheckWin.JapanBookList[i]
                break
        for i in range(0,len(bookCheckWin.ThrillerList)):
            if(data == bookCheckWin.ThrillerList[i].getBookName()):
                del bookCheckWin.ThrillerList[i]
                break
        for i in range(0,len(bookCheckWin.RomanceList)):
            if(data == bookCheckWin.RomanceList[i].getBookName()):
                del bookCheckWin.RomanceList[i]
                break
        for i in range(0,len(bookCheckWin.SFList)):
            if(data == bookCheckWin.SFList[i].getBookName()):
                del bookCheckWin.SFList[i]
                break
        for i in range(0,len(bookCheckWin.FamilyList)):
            if(data == bookCheckWin.FamilyList[i].getBookName()):
                del bookCheckWin.FamilyList[i]
                break
        for i in range(0,len(bookCheckWin.KoreanThrillerList)):
            if(data == bookCheckWin.KoreanThrillerList[i].getBookName()):
                del bookCheckWin.KoreanThrillerList[i]
                break
        for i in range(0,len(bookCheckWin.KoreanRomanceList)):
            if(data == bookCheckWin.KoreanRomanceList[i].getBookName()):
                del bookCheckWin.KoreanRomanceList[i]
                break
        for i in range(0,len(bookCheckWin.KoreanSFList)):
            if(data == bookCheckWin.KoreanSFList[i].getBookName()):
                del bookCheckWin.KoreanSFList[i]
                break
        for i in range(0,len(bookCheckWin.KoreanFamilyList)):
            if(data == bookCheckWin.KoreanFamilyList[i].getBookName()):
                del bookCheckWin.KoreanFamilyList[i]
                break
        for i in range(0,len(bookCheckWin.EnglishThrillerList)):
            if(data == bookCheckWin.EnglishThrillerList[i].getBookName()):
                del bookCheckWin.EnglishThrillerList[i]
                break
        for i in range(0,len(bookCheckWin.EnglishRomanceList)):
            if(data == bookCheckWin.EnglishRomanceList[i].getBookName()):
                del bookCheckWin.EnglishRomanceList[i]
                break
        for i in range(0,len(bookCheckWin.EnglishSFList)):
            if(data == bookCheckWin.EnglishSFList[i].getBookName()):
                del bookCheckWin.EnglishSFList[i]
                break
        for i in range(0,len(bookCheckWin.EnglishFamilyList)):
            if(data == bookCheckWin.EnglishFamilyList[i].getBookName()):
                del bookCheckWin.EnglishFamilyList[i]
                break
        for i in range(0,len(bookCheckWin.JapanThrillerList)):
            if(data == bookCheckWin.JapanThrillerList[i].getBookName()):
                del bookCheckWin.JapanThrillerList[i]
                break
        for i in range(0,len(bookCheckWin.JapanRomanceList)):
            if(data == bookCheckWin.JapanRomanceList[i].getBookName()):
                del bookCheckWin.JapanRomanceList[i]
                break
        for i in range(0,len(bookCheckWin.JapanSFList)):
            if(data == bookCheckWin.JapanSFList[i].getBookName()):
                del bookCheckWin.JapanSFList[i]
                break
        for i in range(0,len(bookCheckWin.JapanFamilyList)):
            if(data == bookCheckWin.JapanFamilyList[i].getBookName()):
                del bookCheckWin.JapanFamilyList[i]
                break  
def showMyReadBookWin(id):
    status_txt = QtGui.QLabel()
    movie = QtGui.QMovie(_fromUtf8(":/UI/loading4.gif"))
    movie.start()
    status_txt.setMovie(movie)
    status_txt.setWindowFlags(QtCore.Qt.CustomizeWindowHint) or status_txt.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    status_txt.show()
    myReadBookWin.setInfo(id)
    status_txt.close()
    myReadBookWin.show()    
def showRecommendWin(id):
    status_txt = QtGui.QLabel()
    movie = QtGui.QMovie(_fromUtf8(":/UI/loading4.gif"))
    movie.start()
    status_txt.setMovie(movie)
    status_txt.setWindowFlags(QtCore.Qt.CustomizeWindowHint) or status_txt.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    status_txt.show()
    recommendWin.setInfo(id)
    status_txt.close()
    recommendWin.show()
def showAllRankWin(id):
    allRankWin.setID(id)
    allRankWin.show()

app.exec_()
s.close()