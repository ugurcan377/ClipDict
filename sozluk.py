#!/usr/bin/python
import sys
import time
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_sozluk import Ui_MainWindow

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
	QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
	self.myClipBoard = QtGui.QApplication.clipboard()
	self.test = self.myClipBoard.text("plain",QtGui.QClipboard.Selection)
	self.url = QtCore.QUrl("http://m.seslisozluk.com/?word=" + self.test)
	self.webView.load(self.url)
	QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.search)
    def search(self):
	self.test = self.lineEdit.text()	
	self.url = QtCore.QUrl("http://m.seslisozluk.com/?word=" + self.test)
	self.webView.load(self.url)

app = QtGui.QApplication(sys.argv)
run = MainWindow()
run.show()
sys.exit(app.exec_())

