import sys,os
import pandas as pd
from pandas.io import data as web
from PyQt4.QtGui import *
from PyQt4 import uic

form_class = uic.loadUiType("MAViewer2.ui")[0]
addevent_class = uic.loadUiType("addEvent.ui")[0]
aboutme_class = uic.loadUiType("aboutMe.ui")[0]

class AddEvent (QDialog, addevent_class):
    date = None
    tag = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setUI()

    def setUI(self):
        self.addButton.clicked.connect(self.addButton_clicked)
        self.closeButton.clicked.connect(self.closeButton_clicked)

    def addButton_clicked(self):
        tmpdate = self.dateEdit.dateTime()
        self.date = tmpdate.toPyDateTime()
        self.tag = self.lineEdit.text()
        self.close()

    def closeButton_clicked(self):
        self.close()

class aboutmeWindow(QDialog,aboutme_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.buttonclicked)
        self.show()
    def buttonclicked(self):
        self.close()




class Window(QMainWindow,form_class):
    compname =""
    data = None

    default = False
    MA5 = False
    MA20 = False
    MA60 = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setUI()
        self.show()
        app.exec_()


    def setUI(self):
        self.fbButton.clicked.connect(self.fbButton_clicked)
        self.teslaButton.clicked.connect(self.teslaButton_clicked)
        self.appleButton.clicked.connect(self.appleButton_clicked)
        self.samsungButton.clicked.connect(self.samsungButton_clicked)
        self.lushButton.clicked.connect(self.lushButton_clicked)
        self.saveButton.clicked.connect(self.saveButton_clicked)
        self.closeButton.clicked.connect(self.cancelButton_clicked)
        self.addEventButton.clicked.connect(self.addEventButton_clicked)

        self.checkBox.stateChanged.connect(self.checkBoxState)
        self.checkBox_2.stateChanged.connect(self.checkBoxState)
        self.checkBox_3.stateChanged.connect(self.checkBoxState)
        self.checkBox_4.stateChanged.connect(self.checkBoxState)

        self.actionNew.triggered.connect(self.clear)
        self.actionSave.triggered.connect(self.saveButton_clicked)
        self.actionClose.triggered.connect(self.close)
        self.actionAbout_Me.triggered.connect(self.aboutme)
    def clear(self):
        self.widget.canvas.ax.clear()
        self.widget.canvas.draw()

    def aboutme(self):
        about_me = aboutmeWindow()
        about_me.exec_()

    def checkBoxState(self):
        if self.checkBox.isChecked():
            self.default = True
        else:
            self.default = False

        if self.checkBox_2.isChecked():
            self.MA5 = True
        else:
            self.MA5 = False

        if self.checkBox_3.isChecked():
            self.MA20 = True
        else:
            self.MA20 = False

        if self.checkBox_4.isChecked():
            self.MA60 = True
        else :
            self.MA60 = False


    def lushButton_clicked(self):
        self.widget.canvas.ax.clear()
        self.compname= "600223.SS"
        self.showGraph()

    def samsungButton_clicked(self):
        self.widget.canvas.ax.clear()
        self.compname = "005930.KS"
        self.showGraph()

    def fbButton_clicked(self):
        self.widget.canvas.ax.clear()
        self.compname = "FB"
        self.showGraph()

    def teslaButton_clicked(self):
        self.widget.canvas.ax.clear()
        self.compname = "TSLA"
        self.showGraph()

    def appleButton_clicked(self):
        self.widget.canvas.ax.clear()
        self.compname = "AAPL"
        self.showGraph()

    def showGraph(self):

        #start = datetime.datetime(2016,1,1)
        #end = datetime.datetime(2017,1,25)

        self.data = web.DataReader(self.compname, "yahoo")
        self.data['MA5'] = pd.rolling_mean(self.data['Adj Close'],5)
        self.data['MA20'] = pd.rolling_mean(self.data['Adj Close'],20)
        self.data['MA60'] = pd.rolling_mean(self.data['Adj Close'],60)
        if self.default == True:
            self.widget.canvas.ax.plot(self.data.index, self.data['Adj Close'], label='Adj Close')
        if self.MA5 ==True:
            self.widget.canvas.ax.plot(self.data.index, self.data['MA5'], label='MA5')
        if self.MA20 == True:
            self.widget.canvas.ax.plot(self.data.index, self.data['MA20'], label='MA20')
        if self.MA60 == True:
            self.widget.canvas.ax.plot(self.data.index, self.data['MA60'], label='MA60')
        self.widget.canvas.draw()



    def saveButton_clicked(self):
        file_choices = "PNG (*.png)|*.png"

        path = QFileDialog.getSaveFileName(self,'Save file', '', file_choices)
        if path:
            self.widget.canvas.print_figure(path)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def cancelButton_clicked(self):
        self.close()


    def addEventButton_clicked(self):
        eventWindow = AddEvent()
        eventWindow.exec_()
        #eventWindow.date, tag
        self.widget.canvas.ax.set_title('Adj Close of '+self.compname)

        if self.compname=="FB" or "APPL":
            a=2
            b=5
        elif self.compname =="005930.KS":
            a=50
            b=200
        elif self.compname =="TSLA":
            a=4
            b=10
        elif self.compname=="600223.SS":
            a=0.2
            b=0.5


        self.widget.canvas.ax.annotate(eventWindow.tag,
                                   xy=(eventWindow.date, self.data['Adj Close'].asof(eventWindow.date)+a) ,
                                                        xytext=(eventWindow.date, self.data['Adj Close'].asof(eventWindow.date)+b),
                                    arrowprops = dict(facecolor='red'),horizontalalignment='left', verticalalignment='top')
        self.widget.canvas.draw()


if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = Window()
    app.exec_()