from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import Ui_ui


class ui_Control(QDialog, Ui_ui):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

"""import sys,os
sys.path.append("/usr/share/qgis/python/")
os.system("export LD_LIBRARY_PATH=/usr/lib/qgis/")
from qgis.core import *
from qgis.gui import *
QgsApplication.setPrefixPath("/usr/", True)
QgsApplication.initQgis()
app=QApplication(sys.argv)
c=ui_Control(None)
c.show()
QgsApplication.exitQgis()
sys.exit(app.exec_())"""
