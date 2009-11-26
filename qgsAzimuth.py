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
        self.fPath = QString()  # set default working directory, updated from config file & by Import/Export
        self.configFile = os.path.join(os.getcwd(),'qgsAz.conf')  # application config file 
        self.loadConf() # get config data
    
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
        self.saveConf()

    def run(self):
        # create and show a configuration dialog or something similar
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        self.pluginGui = ui_Control(self.iface.mainWindow())

        #INSERT EVERY SIGNAL CONECTION HERE!
        QObject.connect(self.pluginGui.pushButton,SIGNAL("clicked()"),self.newVertex)         # insert next segment
        QObject.connect(self.pluginGui.pushButton_2,SIGNAL("clicked()"),self.delrow)           # delete list row
        QObject.connect(self.pluginGui.pushButton_3,SIGNAL("clicked()"),self.loadList)          # import list
        QObject.connect(self.pluginGui.pushButton_6,SIGNAL("clicked()"),self.clearList)         #'Clear List'
        QObject.connect(self.pluginGui.pushButton_7,SIGNAL("clicked()"),self.addgeometry)   # draw object
        QObject.connect(self.pluginGui.pushButton_8,SIGNAL("clicked()"),self.startgetpoint)   # capture starting point from map
        QObject.connect(self.pluginGui.pushButton_9,SIGNAL("clicked()"),self.saveList)          # export list
        
        #reading all layers
        self.layermap=QgsMapLayerRegistry.instance().mapLayers()
        for (name,layer) in self.layermap.iteritems():
            self.pluginGui.comboBox.addItem(name)
        self.pluginGui.tableWidget.setCurrentCell(0,0)
        self.pluginGui.show()
        
        #misc init
        self.magDev = 0.0
        
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
            #warn=QgsMessageViewer()
            #warn.setMessageAsPlainText("Layer not in edit mode.")
            #warn.showMessage()
            self.say("Layer not in edit mode.")
            return 0
        
        # if magnetic heading chosen, assure we have a declination angle
        if (self.pluginGui.radioButton_15.isChecked())  and (str(self.pluginGui.lineEdit_7.text()) == ''):   #magnetic headings      
            #warn=QgsMessageViewer()
            #warn.setMessageAsPlainText("No magnetic declination value entered.")
            #warn.showMessage()
            self.say("No magnetic declination value entered.")
            return 0
        
        vlist=[]
        vlist.append([float(str(self.pluginGui.lineEdit.text())),
                          float(str(self.pluginGui.lineEdit_2.text())), 
                          float(str(self.pluginGui.lineEdit_3.text()))])
        for i in range(self.pluginGui.tableWidget.rowCount()):
            az=str(self.pluginGui.tableWidget.item(i,0).text())
            dis=float(str(self.pluginGui.tableWidget.item(i,1).text()))
            zen=str(self.pluginGui.tableWidget.item(i,2).text())

            #-v-v-v-
            # adjust for input in feet, not meters
            dis = dis/3.281
            #-^-^-^-
            
            #checking degree input
            if (self.pluginGui.radioButton_17.isChecked()):     #angletype='Azimuth'
                az=float(self.dmsToDd(az))
                zen=float(self.dmsToDd(zen))
            elif (self.pluginGui.radioButton_18.isChecked()):   #angletype='Bearing'
                az=float(self.bearingToDd(az))
                zen=float(self.bearingToDd(zen))
        
            #correct for magnetic compass headings if necessary
            if (self.pluginGui.radioButton_13.isChecked()):     # True headings
                self.magDev = 0.0
            elif (self.pluginGui.radioButton_15.isChecked()):   #magnetic headings
                self.magDev = float(self.dmsToDd(str(self.pluginGui.lineEdit_7.text())))
            az = float(az) + float(self.magDev)
        
            #correct for angles outside of 0.0-360.0
            while (az > 360.0):
                az = az - 360.0
            while (az < 0.0):
                az = az + 360.0
        
            #checking survey type
            if (self.pluginGui.radioButton_7.isChecked()):          #surveytype='irradiation'
                vlist.append(self.nextvertex(vlist[0],dis,az,zen))      #reference first vertex
                surveytype='irradiation'
            elif (self.pluginGui.radioButton_8.isChecked()):        #surveytype='polygonal'
                vlist.append(self.nextvertex(vlist[-1],dis,az,zen))     #reference last vertex
                surveytype = 'polygonal'
    
        #reprojecting to projects SRS
        vlist=self.reproject(vlist, vectorlayer)
        
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
        
    def bearingToDd (self,  dms):
        #allow survey bearings in form:  - N 25d 34' 40" E
        #where minus ('-') sign allows handling bearings given in reverse direction
        dms = dms.strip()
        if (dms[0] == '-'):
            rev = True
            dms = dms[1:].strip()
        else:
            rev = False
        
        baseDir = dms[0].upper()
        if (baseDir in ['N','S']):
            adjDir = dms[-1].upper()
            bearing = True
            if (baseDir == 'N'):
                if (adjDir == 'E'):
                    base = 0.0
                    adj = 'add'
                elif (adjDir == 'W'):
                    base = 360.0
                    adj = 'sub'
                else:
                    return 0
            elif (baseDir == 'S'):
                base = 180.0
                if (adjDir == 'E'):
                    adj = 'sub'
                elif (adjDir == 'W'):
                    adj = 'add'
                else:
                    return 0
        else:
            bearing = False

        dd = self.dmsToDd(dms)
 
        if (rev):
            dd = float(dd)+180.0
        
        if (bearing == True):
            if (adj == 'add'):
                dd = float(base) + float(dd)
            elif (adj == 'sub'):
                dd = float(base) - float(dd)

        return dd
 
    def dmsToDd(self,dms):
        "It's not fast, but it's a safe way of dealing with DMS"
        dms=dms.replace(" ", "")
        for c in dms:
            if ((not c.isdigit()) and (c != '.') and (c != '-')):
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
    
    def clearList(self):
        self.pluginGui.tableWidget.clearContents()
        self.pluginGui.tableWidget.setRowCount(0)
    
    def newVertex(self):
        #adds a vertex from the gui
        self.addrow(self.pluginGui.lineEdit_7.text(), self.pluginGui.lineEdit_8.text(), self.pluginGui.lineEdit_9.text())
    
    def addrow(self, az=0, dist=0, zen=90):
        #insert the vertext in the table
        if (self.pluginGui.tableWidget.currentRow()>0):
            i=self.pluginGui.tableWidget.currentRow()
        else:
            i=self.pluginGui.tableWidget.rowCount()
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
        QObject.disconnect(self.tool, SIGNAL("finished(PyQt_PyObject)"), self.getpoint)

    def reproject(self, vlist,  vectorlayer):
        renderer=self.canvas.mapRenderer()
        for i, point in enumerate(vlist):
            vlist[i]= renderer.layerToMapCoordinates(vectorlayer, QgsPoint(point[0], point[1]))
        return vlist

    def setAngle(self, s):
        #self.say('processing angleType='+s)
        if (s=='azimuth'):
            self.pluginGui.radioButton_17.setChecked(True)
        elif (s=='bearing'):
            self.pluginGui.radioButton_18.setChecked(True)
        elif (s=='polar'):
            self.pluginGui.radioButton_16.setChecked(True)
        else:
            self.say('invalid angle type: '+s)
    
    def setHeading(self,  s):
        #self.say('processing headingType='+s)
        if (s=='true'):
            self.pluginGui.radioButton_13.setChecked(True)
        elif (s=='magnetic'):
            self.pluginGui.radioButton_15.setChecked(True)
        else:
            self.say('invalid heading type: '+s)
            
    def setDeclination(self,  s):    
        #self.say('processing declination='+s)
        #TODO - we need a proper field for this
        self.pluginGui.lineEdit_7.setText(s)
        self.magDev = float(s)

    def setStartAt(self,  s):
        #self.say('processing startAt='+s)
        coords=s.split(';')
        self.pluginGui.lineEdit.setText(coords[0])
        self.pluginGui.lineEdit_2.setText(coords[1])
        self.pluginGui.lineEdit_3.setText(coords[2])
    
    def setSurvey(self, s):
        #self.say('processing surveyType='+s)
        if (s=='polygonal'):
            self.pluginGui.radioButton_8.setChecked(True)
        elif (s=='irradiate'):
            self.pluginGui.radioButton_7.setChecked(True)
        else:
            self.say('invalid survey type: '+s)
    
    def say(self, txt):
        warn=QgsMessageViewer()
        warn.setMessageAsPlainText(txt)
        warn.showMessage()
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    #               File handling
    # This section deals with saving the user data to disk, and loading it
    #
    # format:
    #   line 1: angle=Azimuth|Bearing|Polar
    #   line 2: heading=True|Magnetic
    #   line 3: declination=[- ]x.xxd[ xx.x'] [E|W]
    #   line 4: startAt=xxxxx.xxxxx, xxxxxx.xxxxx
    #   line 5: survey=Polygonal|Irradiat
    #   line 6: [data]
    #   line 7 through end: Azimuth; dist; zen
    #
    #       note: lines 1 through 5 are optional if hand entered, but will always be generated when 'saved'
    # ---------------------------------------------------------------------------------------------------------------------------------
    def loadList(self):
        file=QFileDialog.getOpenFileName(None,"Load data separated by ';'",self.fPath,QString(),None)
        if not os.path.exists(file):
            return 0
        # update selected file's folder
        fInfo = QFileInfo(file)
        self.fPath = fInfo.absolutePath ()
        self.saveConf()

        # get saved data
        f=open(file)
        lines=f.readlines()
        f.close()
        for line in lines:
            #remove trailing 'new lines', etc and break into parts
            parts = ((line.strip()).lower()).split("=")
            if (len(parts)>1):
                #self.say("line="+line+'\nparts[0]='+parts[0]+'\nparts[1]='+parts[1])
                if (parts[0].lower()=='angle'):
                    self.setAngle(parts[1].lower())
                elif (parts[0].lower()=='heading'):
                    self.setHeading(parts[1].lower())
                elif (parts[0].lower()=='declination'):
                    self.setDeclination(parts[1].lower())
                elif (parts[0].lower()=='startat'):
                    self.setStartAt(parts[1].lower())
                elif (parts[0].lower()=='survey'):
                    self.setSurvey(parts[1].lower())
            else:
                coords=(line.strip()).split(";")
                if (coords[0].lower()=='[data]'):
                    pass
                else:
                    self.addrow(coords[0], coords[1], coords[2])
   
    def saveList(self):
        file=QFileDialog.getSaveFileName(None,"Save segment list to file.",self.fPath,QString(),None)
        f=open(file, 'w')
        # update selected file's folder
        fInfo = QFileInfo(file)
        self.fPath = fInfo.absolutePath ()
        self.saveConf()
        
        if (self.pluginGui.radioButton_17.isChecked()): 
            s='Azimuth'
        elif (self.pluginGui.radioButton_18.isChecked()):
            s='Bearing'
        f.write('angle='+s+'\n') 
        
        if (self.pluginGui.radioButton_13.isChecked()):
            s='True'
        elif (self.pluginGui.radioButton_15.isChecked()):
            s='Magnetic'
        f.write('heading='+s+'\n') 
        
        if (self.magDev!=0.0):
            f.write('declination='+str(self.magDev)+'\n')
        
        f.write('startAt='+str(self.pluginGui.lineEdit.text())+';'+str(self.pluginGui.lineEdit_2.text())+';'+str(self.pluginGui.lineEdit_3.text())+'\n')

        if (self.pluginGui.radioButton_8.isChecked()):
            s='Polygonal'
        elif (self.pluginGui.radioButton_7.isChecked()):
            s='Irradiate'
        f.write('survey='+s+'\n') 
        
        f.write('[data]\n')
        for i in range(self.pluginGui.tableWidget.rowCount()):
            line = str(self.pluginGui.tableWidget.item(i, 0).text()) +';'+str(self.pluginGui.tableWidget.item(i, 1).text()) +';'+str(self.pluginGui.tableWidget.item(i, 2).text())
            f.write(line+'\n')
            
        f.close()
    
    #------------------------
    def loadConf(self):
        #self.say("getting config data from "+self.configFile)
        if os.path.exists(self.configFile):
            f=open(self.configFile)
            lines=f.readlines()
            for line in lines:
                #self.say("found '"+line+"'")
                parts = (line.strip()).split('=')
                if (parts[0]=='inp_exp_dir'):
                    self.fPath = parts[1]
                    #self.say("found config file:\n inp/exp dir='"+self.fPath+"' in "+self.configFile)
            f.close()
        else:
            self.fPath = QString()
        

    def saveConf(self):
        f=open(self.configFile, 'w')
        #self.say("saving '"+self.fPath+"' to "+self.configFile)
        try:
            line = 'inp_exp_dir='+self.fPath+'\n'
            f.write(line)
        except:
            import sys
            self.say("Unable to write to file '"+self.configFile+"':\n"+str(sys.exc_info()[0])+str(sys.exc_info()[1]))
        f.close()
