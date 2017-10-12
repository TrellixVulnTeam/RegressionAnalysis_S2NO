import sys
from PyQt5.QtWidgets import QApplication
from gui import XMainWindow


#gui
app = QApplication(sys.argv)
dlg = XMainWindow()
dlg.show()
app.exec_()