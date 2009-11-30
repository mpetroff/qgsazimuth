from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_ui import Ui_ui


class ui_Control(QDialog, Ui_ui):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

if __name__=="__main__":
    import sys,os
    app=QApplication(sys.argv)
    c=ui_Control(None)
    c.show()
    sys.exit(app.exec_())
