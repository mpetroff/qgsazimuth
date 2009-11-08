#---------------------------------------------------------------------
# 
# licensed under the terms of GNU GPL 2
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
#---------------------------------------------------------------------

import os,sys
sys.path.append("/usr/share/qgis/python")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from ui_control import ui_Control
import resources
from math import *
from getcoordtool import *

class qgsazimuth:

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        
    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon(":qgsazimuth.png"), "Azimuth and distance", self.iface.mainWindow())
        self.action.setWhatsThis("Azimuth and distance")
        QObject.connect(self.action, SIGNAL("activated()"), self.run)
        # add toolbar button and menu item
        #self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Topography", self.action)
        
        self.tool = GetCoordTool(self.canvas)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&Topography",self.action)
        self.iface.removeToolBarIcon(self.action)

    
    
    def run(self):
        # create and show a configuration dialog or something similar
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        self.pluginGui = ui_Control(self.iface.mainWindow())

        #INSERT EVERY SIGNAL CONECTION HERE!
        QObject.connect(self.pluginGui.pushButton_7,SIGNAL("clicked()"),self.addgeometry)
        QObject.connect(self.pluginGui.pushButton,SIGNAL("clicked()"),self.newVertex)
        QObject.connect(self.pluginGui.pushButton_2,SIGNAL("clicked()"),self.delrow)
        QObject.connect(self.pluginGui.pushButton_8,SIGNAL("clicked()"),self.startgetpoint)
        QObject.connect(self.pluginGui.pushButton_3,SIGNAL("clicked()"),self.loadList)
        #reading all layers
        self.layermap=QgsMapLayerRegistry.instance().mapLayers()
        for (name,layer) in self.layermap.iteritems():
            self.pluginGui.comboBox.addItem(name)
        self.pluginGui.tableWidget.setCurrentCell(0,0)
        self.pluginGui.show()
    
    
    #Now these are the SLOTS
    def nextvertex(self,v,d,az,zen=90):
        print "direction:", az, zen, d
        az=radians(az)
        zen=radians(zen)
        d1=d*sin(zen)
        x=v[0]+d1*sin(az)
        y=v[1]+d1*cos(az)
        z=v[2]+d*cos(zen)
        print "point ", x,y,z
        return [x,y,z]
    
    def addgeometry(self):
        #reading a layer
        print "Saving in "+self.pluginGui.comboBox.currentText()
        vectorlayer=self.layermap[self.pluginGui.comboBox.currentText()]
        provider=vectorlayer.dataProvider()
        geometrytype=provider.geometryType()
        print geometrytype
        #check if the layer is editable
        if (not vectorlayer.isEditable()):
            warn=QgsMessageViewer()
            warn.setMessageAsPlainText("Layer not in edit mode.")
            warn.showMessage()
            return 0
        vlist=[]
        vlist.append([float(str(self.pluginGui.lineEdit.text())) ,float(str(self.pluginGui.lineEdit_2.text())),         float(str(self.pluginGui.lineEdit_3.text()))])
        for i in range(0,self.pluginGui.tableWidget.rowCount()):
            zen=str(self.pluginGui.tableWidget.item(i,2).text())
            az=str(self.pluginGui.tableWidget.item(i,0).text())
            d=float(str(self.pluginGui.tableWidget.item(i,1).text()))
            #checking degree input
            if (self.pluginGui.radioButton_11.isChecked()): #inputtype='DD'
                az=float(az)
                zen=float(zen)
            elif (self.pluginGui.radioButton_12.isChecked()): #inputtype='DMS'
                az=float(self.dmsToDd(az))
                zen=float(self.dmsToDd(zen))
            #checking survey type
            if (self.pluginGui.radioButton_7.isChecked()): #surveytype='irradiation'
                vlist.append(self.nextvertex(vlist[0],d,az,zen))#reference first vertex
            elif (self.pluginGui.radioButton_8.isChecked()): #surveytype='polygonal'
                vlist.append(self.nextvertex(vlist[-1],d,az,zen))#reference last vertex
        featurelist=[]
        if (geometrytype==1): #POINT
            for point in vlist:
                #writing new feature
                p=QgsPoint(point[0],point[1])
                geom=QgsGeometry.fromPoint(p)
                feature=QgsFeature()
                feature.setGeometry(geom)
                featurelist.append(feature)
        elif (geometrytype==2): #LINESTRING
            if (surveytype== 'polygonal'):
                pointlist=[]
                for point in vlist:
                    #writing new feature
                    p=QgsPoint(point[0],point[1])
                    pointlist.append(p)
                geom=QgsGeometry.fromPolyline(pointlist)
                feature=QgsFeature()
                feature.setGeometry(geom)
                featurelist.append(feature)
            elif (surveytype=='irradiation'):
                v0=vlist.pop(0)
                v0=QgsPoint(v0[0],v0[1])
                for point in vlist:
                    #writing new feature
                    p=QgsPoint(point[0],point[1])
                    pointlist=[v0,p]
                    geom=QgsGeometry.fromPolyline(pointlist)
                    feature=QgsFeature()
                    feature.setGeometry(geom)
                    featurelist.append(feature)
        elif (geometrytype==3): #POLYGON
            pointlist=[]
            for point in vlist:
                #writing new feature
                p=QgsPoint(point[0],point[1])
                pointlist.append(p)
            geom=QgsGeometry.fromPolygon([pointlist])
            feature=QgsFeature()
            feature.setGeometry(geom)
            featurelist.append(feature)
        
        #commit
        vectorlayer.addFeatures(featurelist)
        self.iface.mapCanvas().zoomToSelected()
        
    def dmsToDd(self,dms):
        "It's not fast, but it's a safe way of dealing with DMS"
        dms=dms.replace(" ", "")
        for c in dms:
            if not c.isdigit():
                dms=dms.replace(c,';')
        while (dms.find(";;")>=0):
            dms=dms.replace(";;",';')
        if dms[0]==';':
            dms=dms[1:]
        dms=dms.split(";")
        dd=0
        for i, f in enumerate(dms):
            if f!="":
                dd+=float(f)/pow(60, i)
        #dd=str(float(dms[0])+float(dms[1])/60+float(dms[2])/3600)
        return dd
    
    def loadList(self):
        file=QFileDialog.getOpenFileName(None,"Load data separated by ';'",QString(),QString(),None)
        if not os.path.exists(file):
            return 0
        f=open(file)
        lines=f.readlines()
        f.close()
        for line in lines:
            coords=line.split(";")
            self.addrow(coords[0], coords[1], coords[2])
        pass
    
    def newVertex(self):
        #adds a vertex from the gui
        self.addrow(self.pluginGui.lineEdit_7.text(), self.pluginGui.lineEdit_8.text(), self.pluginGui.lineEdit_9.text())
    
    def addrow(self, az=0, dist=0, zen=90):
        #insert the vertext in the table
        if (self.pluginGui.tableWidget.currentRow()>0):
            i=self.pluginGui.tableWidget.currentRow()
        else:
            i=0
        self.pluginGui.tableWidget.insertRow(i)
        self.pluginGui.tableWidget.setItem(i, 0, QTableWidgetItem(str(az)))
        self.pluginGui.tableWidget.setItem(i, 1, QTableWidgetItem(str(dist)))
        self.pluginGui.tableWidget.setItem(i, 2, QTableWidgetItem(str(zen)))
        #print self.pluginGui.tableWidget.item(i+1,1).text()#.setText("90")
        
    def delrow(self):
        self.pluginGui.tableWidget.removeRow(self.pluginGui.tableWidget.currentRow())
        
    def moveup(self):
        pass
    
    def movedown(self):
        pass
    
    def startgetpoint(self):
        #point capture tool
        QObject.connect(self.tool, SIGNAL("finished(PyQt_PyObject)"), self.getpoint)
        self.saveTool = self.canvas.mapTool()
        self.canvas.setMapTool(self.tool)

    def getpoint(self,pt):
        self.pluginGui.lineEdit.setText(str(pt.x()))
        self.pluginGui.lineEdit_2.setText(str(pt.y()))
        self.canvas.setMapTool(self.saveTool)
        QObject.disconnect(self.tool, SIGNAL("finished(PyQt_PyObject)"),
                       self.getpoint)
