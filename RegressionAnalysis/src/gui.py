from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from layout import Ui_MainWindow
from Regression import regression, polynomial_regression
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


class XMainWindow(QMainWindow, Ui_MainWindow):
    x_data = []
    y_data = []
    option = {}

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # making matplot canvas
        self.figure = plt.Figure()
        self.canvas = MyFigureCanvas(self.figure,self)
        self.figuareLayout.addWidget(self.canvas)
        self.axes_subplot = self.figure.add_subplot(111)

        self.axesInit()

        # event handler
        self.dial.valueChanged.connect(self.dialChanged_Event)
        self.clearButton.clicked.connect(self.clearButtonClicked_Event)
        self.excuteButton.clicked.connect(self.excuteButtonClick_Event)
        self.actionGoto_gitHub.triggered.connect(lambda: webbrowser.open("https://github.com/NarciSource/RegressionAnalysis"))
        self.actionAbout.triggered.connect(self.actionAbout_Event)
        self.actionExit.triggered.connect(self.close)
        
        # regression option
        self.option = {"hyper": 0,
                       "learning_rate": 0.01,
                       "steps": 500}
    
    def axesInit(self):
        self.axes_subplot.clear()
        self.axes_subplot.set_xlim(-2,2)
        self.axes_subplot.set_ylim(-30, 120)
        self.axes_subplot.set_xlabel('x')
        self.axes_subplot.set_ylabel('y')
        self.axes_subplot.legend(loc=0)


    ## process method
    def core(self):
        order_level = 10

        for order in range(2, order_level):
            esst_weights = polynomial_regression(self.y_data, self.x_data, order, option=self.option)
            self.draw_line(order, esst_weights)

        self.draw()


    def draw(self):
        self.canvas.draw()


    def draw_line(self, order, weights):
        smoth = 100
        line_xlim, line_ylim = (-10,10)

        line_data = np.linspace(line_xlim,line_ylim,smoth)

        draw_x_data = [[pow(x, order) for x in line_data] for order in range(0, order)]
        draw_y_data = np.dot(weights, draw_x_data)

        self.axes_subplot.plot(line_data, np.transpose(draw_y_data),label = str(order-1)+" order")
        print(str(order)+": "+str(weights))
        


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

        self.axes_subplot.plot(self.x_data, self.y_data, 'ro')
        self.draw()


    ## event handler
    def excuteButtonClick_Event(self):
        self.core()

    def clearButtonClicked_Event(self):
        self.x_data = []
        self.y_data = []
        self.axesInit()
        self.draw()

    def actionAbout_Event(self):
        msgbox = QMessageBox(self)
        msgbox.information(self,"About","Chung Ang Univ\nName : Jeong Won Cheol\nStudent Code : 20113560")

    def dialChanged_Event(self):
        self.option["hyper"] = self.dial.value()
        regression(self.x_data, self.y_data, order_hat=4, paper=self.axes_subplot, option=self.option)
        self.draw()

    def mousePosition_onCanvas_Event(self, event):
        self.data_factory(event.x(), event.y())        

    def mouseWheel_onCanvas_Event(self, event):
        wheelup,wheeldown = (120,-120)
        rate = 0.1
        if event.angleDelta().y() == wheelup:
            xlim_begin,xlim_end = self.axes_subplot.get_xlim()
            ylim_begin,ylim_end = self.axes_subplot.get_ylim()
            self.axes_subplot.set_xlim(xlim_begin*(1-rate),xlim_end*(1-rate))
            self.axes_subplot.set_ylim(ylim_begin*(1-rate),ylim_end*(1-rate))
            self.draw()
        elif event.angleDelta().y() == wheeldown:
            xlim_begin,xlim_end = self.axes_subplot.get_xlim()
            ylim_begin,ylim_end = self.axes_subplot.get_ylim()
            self.axes_subplot.set_xlim(xlim_begin*(1+rate),xlim_end*(1+rate))
            self.axes_subplot.set_ylim(ylim_begin*(1+rate),ylim_end*(1+rate))
            self.draw()


class MyFigureCanvas(FigureCanvas):
    def __init__(self,figure,object):
        super().__init__(figure)
        self.object = object
    def mousePressEvent(self, event):
        self.object.mousePosition_onCanvas_Event(event)
    def wheelEvent(self, event):        
        self.object.mouseWheel_onCanvas_Event(event)