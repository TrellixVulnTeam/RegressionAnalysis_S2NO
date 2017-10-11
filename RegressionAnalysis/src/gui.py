from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from layout import Ui_MainWindow
from Regression import regression, polynomial_regression
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


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
        self.option = {"hyper": 0,
                       "learning_rate": 0.001,
                       "steps": 500}

    def excuteButtonClick_Event(self):
        self.core()

    def core(self):
        degree_level = 10

        for degree in range(1, degree_level):
            esst_weights = polynomial_regression(self.x_data, self.y_data, degree, paper=self.axes_subplot, option=self.option)
            self.plotf(degree, esst_weights)

        self.draw()


    def plotf(self, degree_hat, weights):
        draw_x_data = [[0 for col in range(100)] for row in range(degree_hat)]
        draw_x_data[0] = np.linspace(-10,10,100)


        for i in range(100):
            for j in range(degree_hat-1):
                draw_x_data[j+1][i] = pow(draw_x_data[0][i],j+2)

        draw_y_data = np.dot(weights, draw_x_data)

        self.axes_subplot.plot(draw_x_data[0], np.transpose(draw_y_data),label = degree_hat)
        print(weights)
        

    def draw(self):
        self.axes_subplot.plot(self.x_data, self.y_data, 'ro')
        self.axes_subplot.set_xlim(-2,2)
        self.axes_subplot.set_ylim(-30, 120)
        self.axes_subplot.set_xlabel('x')
        self.axes_subplot.set_ylabel('y')
        self.axes_subplot.legend(loc=0)

        self.canvas.draw()


      #  self.axes_subplot.clear()
      #  self.canvas.draw()

    def dialChanged_Event(self):
        self.option["hyper"] = self.dial.value()
        regression(self.x_data, self.y_data, degree_hat=4, paper=self.axes_subplot, option=self.option)

        self.draw()


class MyFigureCanvas(FigureCanvas):
    def __init__(self,figure,object):
        super().__init__(figure)
        self.object = object
    def mousePressEvent(self, event):
        print(event.x(), event.y())
        
        print(self.axes_subplot.xaxis, self.axes_subplot.yaxis)
        print(self.figure.get_figheight(), self.figure.get_figwidth())
