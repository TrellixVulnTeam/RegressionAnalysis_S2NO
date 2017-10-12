from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from layout import Ui_MainWindow
from regression import regression, polynomial_regression
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import math
import webbrowser


class XMainWindow(QMainWindow, Ui_MainWindow):
    order_level = 10+1
    x_data = []
    y_data = []
    option = {}
    result = {} # [weights,error_rate]

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # making matplot canvas
        self.figure = plt.Figure()
        self.canvas = MyFigureCanvas(self.figure,self)
        self.figuareLayout.addWidget(self.canvas)
        self.axes_subplot = self.figure.add_subplot(111)

        self.axesInit()

        # regression option
        self.option = {"learning_rate": 0.01,
                       "steps": 500,
                       "regularization": "ridge",
                       "hyper": 0,
                       "hyper2": 0}

        self.result = dict([i,[[],0]] for i in range(0,self.order_level))

        # event handler
        self.dial.valueChanged.connect(self.dialChanged_Event)
        self.dial_2.valueChanged.connect(self.dial2Changed_Event)
        self.clearButton.clicked.connect(self.clearButtonClicked_Event)
        self.excuteButton.clicked.connect(self.excuteButtonClick_Event)
        self.actionGoto_gitHub.triggered.connect(lambda: webbrowser.open("https://github.com/NarciSource/RegressionAnalysis"))
        self.actionAbout.triggered.connect(self.actionAbout_Event)
        self.learningrateEdit.textChanged.connect(self.lEditChanged_Event)
        self.stepsEdit.textChanged.connect(self.stepsEditChanged_Event)
        self.comboBox.currentIndexChanged.connect(self.comboBoxChanged_Event)
        self.actionExit.triggered.connect(self.close)
        self.radioButton.clicked.connect(self.radioButtonClicked_Event)
        self.radioButton_2.clicked.connect(self.radioButtonClicked_Event)
        self.radioButton_3.clicked.connect(self.radioButtonClicked_Event)
        
        for i in range(2, self.order_level):
            self.comboBox.addItem(str(i)+" polynomial")


    def axesInit(self):
        self.axes_subplot.clear()
        self.axes_subplot.set_title("Regression analysis Plot")
        self.axes_subplot.set_xlim(-2,2)
        self.axes_subplot.set_ylim(-30, 120)
        self.axes_subplot.set_xlabel('x')
        self.axes_subplot.set_ylabel('y')
        self.axes_subplot.legend(loc=0)


    ## process method
    def core(self):
        for order in range(1, self.order_level):
            self.result[order] = polynomial_regression(self.y_data, self.x_data, order, option=self.option)
        

    def draw(self):
        self.canvas.draw()


    def draw_line(self, num):
        smoth = 100
        line_xlim, line_ylim = (-10,10)

        line_data = np.linspace(line_xlim,line_ylim,smoth)
        weight = self.result[num][0]

        if num is 0:
            for i in range(1,self.order_level):
                self.draw_line(i)
        elif len(weight) is not 0:
            draw_x_data = [[pow(x, order) for x in line_data] for order in range(0, num+1)]
            draw_y_data = np.dot(weight, draw_x_data)

            print(str(num)+": "+str(weight))
            self.axes_subplot.plot(line_data, np.transpose(draw_y_data),label = str(num)+" order")
        else:
            None

    def draw_point(self):
        self.axes_subplot.plot(self.x_data, self.y_data, 'ro')

    def data_factory(self, point_x, point_y):
        margin_bottom, margin_left = (54,60)
        canvas_width, canvas_height = (374,374)
        canvas_xlim_start, canvas_xlim_end = self.axes_subplot.get_xlim()
        canvas_xlim_length = canvas_xlim_end - canvas_xlim_start
        canvas_ylim_start, canvas_ylim_end = self.axes_subplot.get_ylim()
        canvas_ylim_length = canvas_ylim_end - canvas_ylim_start

        x= (point_x-margin_left)/canvas_width*canvas_xlim_length + canvas_xlim_start
        y= (self.figure.get_figheight()*100-point_y-margin_bottom)/canvas_height*canvas_ylim_length + canvas_ylim_start

        self.x_data.append(x)
        self.y_data.append(y)

        self.draw_point()
        self.draw()


    ## event handler
    def excuteButtonClick_Event(self):
        self.axesInit()
        self.core()
        self.draw_point()
        self.draw_line(0) # 0 is all
        self.draw()        

    def clearButtonClicked_Event(self):
        self.x_data = []
        self.y_data = []
        self.axesInit()
        self.draw()

    def dialChanged_Event(self):
        self.dialLabel.setText(str(self.dial.value()/10))
        self.option["hyper"] = self.dial.value()/10

    def dial2Changed_Event(self):
        self.dialLabel2.setText(str(self.dial_2.value()/10))
        self.option["hyper2"] = self.dial_2.value()/10

    def comboBoxChanged_Event(self, item):
        print(self.result[item][1])
        if not math.isnan(self.result[item][1]):
            self.errorrateLCD.display(self.result[item][1])
        else:
            self.errorrateLCD.display("NAN")
        self.axesInit()
        self.draw_point()
        self.draw_line(item)
        self.draw()

    def mouseWheel_onCanvas_Event(self, event):
        wheelup,wheeldown = (120,-120)
        xlim_begin,xlim_end = self.axes_subplot.get_xlim()
        ylim_begin,ylim_end = self.axes_subplot.get_ylim()
        rate = 0.1
        if event.angleDelta().y() == wheelup:
            self.axes_subplot.set_xlim(xlim_begin*(1-rate),xlim_end*(1-rate))
            self.axes_subplot.set_ylim(ylim_begin*(1-rate),ylim_end*(1-rate))
            self.draw()
        elif event.angleDelta().y() == wheeldown:
            self.axes_subplot.set_xlim(xlim_begin*(1+rate),xlim_end*(1+rate))
            self.axes_subplot.set_ylim(ylim_begin*(1+rate),ylim_end*(1+rate))
            self.draw()

    def mousePosition_onCanvas_Event(self, event):
        self.data_factory(event.x(), event.y())  

    def actionAbout_Event(self):
        msgbox = QMessageBox(self)
        msgbox.information(self,"About","Chung Ang Univ\nName : Jeong Won Cheol\nStudent Code : 20113560")

    def lEditChanged_Event(self):
        self.option["learning_rate"] = float(self.learningrateEdit.text())

    def stepsEditChanged_Event(self):
        self.option["steps"] = int(self.stepsEdit.text())

    def radioButtonClicked_Event(self):
        self.dial_2.setEnabled(False)
        self.dial_2.setNotchesVisible(False)
        if self.radioButton.isChecked():
            self.option["regularization"] = "ridge"
        elif self.radioButton_2.isChecked():
            self.option["regularization"] = "lasso"
        elif self.radioButton_3.isChecked():
            self.option["regularization"] = "elastic_net"
            self.dial_2.setEnabled(True)
            self.dial_2.setNotchesVisible(True)

class MyFigureCanvas(FigureCanvas):
    def __init__(self,figure,object):
        super().__init__(figure)
        self.object = object
    def mousePressEvent(self, event):
        self.object.mousePosition_onCanvas_Event(event)
    def wheelEvent(self, event):        
        self.object.mouseWheel_onCanvas_Event(event)