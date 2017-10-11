from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from layout import Ui_MainWindow
from Regression import regression
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class XMainWindow(QMainWindow, Ui_MainWindow):


    def __init__(self, x_data, y_data):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.x_data = x_data
        self.y_data = y_data
        
        self.figure = plt.Figure()
        self.canvas = MyFigureCanvas(self.figure,self)
        self.figuareLayout.addWidget(self.canvas)

        self.axes_subplot = self.figure.add_subplot(111)
        
        self.dial.valueChanged.connect(self.dialChanged_Event)
        self.excuteButton.clicked.connect(self.excuteButtonClick_Event)
        self.option = {"hyper": 0}

    def excuteButtonClick_Event(self):
        degree_level = 10

        for degree in range(1, degree_level):
             regression(self.x_data, self.y_data, degree_hat=degree, paper=self.axes_subplot, option=self.option)

        self.draw()

        

    def draw(self):
        self.axes_subplot.plot(self.x_data, self.y_data, 'ro')
        self.axes_subplot.set_xlim(-2,2)
        self.axes_subplot.set_ylim(-30, 120)
        self.axes_subplot.set_xlabel('x')
        self.axes_subplot.set_ylabel('y')

        self.canvas.draw()


      #  self.axes_subplot.clear()
      #  self.canvas.draw()

    def dialChanged_Event(self):
        self.option["hyper"] = self.dial.value()
        regression(self.x_data, self.y_data, degree_hat=4, paper=self.axes_subplot, option=self.option)

        self.draw()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            print("haha")



class MyFigureCanvas(FigureCanvas):
    def __init__(self,figure,object):
        super().__init__(figure)
        self.object = object
    def mousePressEvent(self, event):
        self.object.mousePressEvent(event)