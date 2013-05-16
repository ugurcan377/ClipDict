#!/usr/bin/python
# coding: utf-8
""" <programın adını ve ne yaptığını özetleyen bir satır.>
   Copyright (C) 2013 Uğurcan Ergün ugurcanergn<at>gmail.com

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA"""

import sys
import time
import urllib2
import json
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_sozluk import Ui_MainWindow

API_KEY = ""

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.api_key = API_KEY
        self.lang_dict = {u"Ingilizce-Turkce":{"from" : "en", "to" : "tr"}, u"Turkce-Ingilizce":{"from" : "tr", "to" : "en"}}

        self.pushButton.clicked.connect(self.buttons_clicked)
        self.pushButton_2.clicked.connect(self.buttons_clicked)
        self.comboBox_init()
        self.comboBox.setCurrentIndex(0)

        self.myClipBoard = QtGui.QApplication.clipboard()
        self.query = str(self.get_query())
        res = self.make_request()
        self.meanings = self.get_json(res)
        self.show_data()


    def get_query(self):
        selection = self.myClipBoard.text("plain",QtGui.QClipboard.Selection)
        self.lineEdit.setText(selection)
        return selection

    def make_request(self):
        lang_pair = self.comboBox.currentText()
        if (len(self.query) < 30):
            req_str = "http://api.seslisozluk.com/?key=%s&lang_from=%s&lang_to=%s&query=%s&callback=?" %(self.api_key,self.lang_dict[str(lang_pair)]["from"], self.lang_dict[str(lang_pair)]["to"], self.query.replace("\n",""))
            print req_str
            req = urllib2.Request(req_str)
            response = urllib2.urlopen(req)
            return response.read()

    def get_json(self,query_result):
    # Seslisozluk api returns a json starts with "?(" and ends with ")"
    # to make python json library to do its trick i had to remove these chars
        return json.loads(query_result[2:-1]) #returns a list of dicts

    def show_data(self):
        self.listWidget.clear()
        self.listWidget.addItem("Aranan Kelime: %s"%(self.meanings[u"query"]))
        count = 1
        try:
            for elem in self.meanings[u"translations"]:
                self.listWidget.addItem("%i-) %s"%(count,elem[u"translation"]))
                count += 1
        except TypeError:
            pass

    def buttons_clicked(self):
        if (self.sender().objectName == self.pushButton.objectName):
            self.query = self.lineEdit.text()
        else:
            self.query = self.get_query()
        res_event = self.make_request()
        self.meanings = self.get_json(res_event)
        self.show_data()

    def comboBox_init(self):
        for key in self.lang_dict.keys():
            self.comboBox.addItem(key)

app = QtGui.QApplication(sys.argv)
run = MainWindow()
run.show()
sys.exit(app.exec_())

