import sys
from PyQt5.QtWidgets import QApplication
from gui import XMainWindow
from data_factory import factory


x_data,y_data = factory()


#gui
app = QApplication(sys.argv)
dlg = XMainWindow(x_data, y_data)
dlg.show()
app.exec_()