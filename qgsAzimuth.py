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

class qgsazimuth (object):
    """
    Base class for the qgsAzimuth plugin
    - Provides a means to draw a feature by specifying the angle and distance beetween points.
    - Supports angles in either the conventional 0.0 - 360.0 clockwise from North
        or the surveyor's 'Easting' system with bearings plus or minus 90 deg. from North or South
    - Supports magnetic declination as degrees plus or minus for East or West respectively
    - supports inputs in feet or the current CRS units
    """

    # just a test to see if mods are taking

    def __init__(self, iface):
        self.iface = iface
        self.legend = iface.legendInterface()
        self.canvas = iface.mapCanvas()
        self.fPath = ""  # set default working directory, updated from config file & by Import/Export

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon(":qgsazimuth.png"), "Azimuth and distance", self.iface.mainWindow())
        self.action.setWhatsThis("Azimuth and distance")
        self.action.triggered.connect(self.run)

        # add toolbar button and menu item
        self.iface.addPluginToMenu("&Topography", self.action)
        self.pluginGui = ui_Control(self.iface.mainWindow())

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

        #misc init
        self.loadConf() # get config data
        self.clearList()
        self.setDeclination('0.0')
        self.setStartAt("0;0;90")    # remove previous StartAt point

        #INSERT EVERY SIGNAL CONECTION HERE!
        self.pluginGui.pushButton_vertexAdd.clicked.connect(self.addRow)
        self.pluginGui.pushButton_vertexInsert.clicked.connect(self.insertRow)
        self.pluginGui.pushButton_segListRowDel.clicked.connect(self.delRow)
        self.pluginGui.pushButton_segListLoad.clicked.connect(self.loadList)
        self.pluginGui.pushButton_segListClear.clicked.connect(self.clearList)
        self.pluginGui.pushButton_objectDraw.clicked.connect(self.addgeometry)
        self.pluginGui.pushButton_startCapture.clicked.connect(self.startgetpoint)
        self.pluginGui.pushButton_segListSave.clicked.connect(self.saveList)

        self.pluginGui.lineEdit_crs.setText(self.iface.mapCanvas().mapRenderer().destinationCrs().description())

        self.pluginGui.table_segmentList.setCurrentCell(0,0)
        if self.iface.activeLayer():
            self.updatelayertext(self.iface.activeLayer())
            self.pluginGui.radioButton_useActiveLayer.setChecked(True)
        else:
            self.pluginGui.radioButton_useActiveLayer.setEnabled(False)
            self.pluginGui.radioButton_useMemoryLayer.setChecked(True)
        self.legend.currentLayerChanged.connect(self.updatelayertext)
        self.pluginGui.show()

        # for debugging convenience
        self.notes = self.pluginGui.plainTextEdit_note

    def updatelayertext(self, layer):
        if not layer:
            self.pluginGui.radioButton_useActiveLayer.setEnabled(False)
        else:
            self.pluginGui.radioButton_useActiveLayer.setEnabled(True)
            self.pluginGui.radioButton_useActiveLayer.setText("Active Layer ({0})".format(layer.name()))

    #Now these are the SLOTS
    def nextvertex(self,v,d,az,zen=90):
        #print "direction:", az, zen, d
        az=radians(az)
        zen=radians(zen)
        d1=d*sin(zen)
        x=v[0]+d1*sin(az)
        y=v[1]+d1*cos(az)
        z=v[2]+d*cos(zen)
        #print "point ", x,y,z
        return [x,y,z]

    @property
    def useactivelayer(self):
        return self.pluginGui.radioButton_useActiveLayer.isChecked()

    def addgeometry(self):
        #initialization
        s = QSettings()
        if self.useactivelayer:
            vectorlayer = self.iface.activeLayer()
        else:
            oldValidation = s.value("/Projections/defaultBehaviour", "useProject")
            s.setValue("/Projections/defaultBehaviour", "useProject")
            vectorlayer=QgsVectorLayer("LineString", "tmp_plot", "memory")
            s.setValue("/Projections/defaultBehaviour", oldValidation)

        provider=vectorlayer.dataProvider()
        geometrytype=provider.geometryType()

        # if magnetic heading chosen, assure we have a declination angle
        if (self.pluginGui.radioButton_magNorth.isChecked())  and (str(self.pluginGui.lineEdit_magNorth.text()) == ''):   #magnetic headings
            self.say("No magnetic declination value entered.")
            return 0

        #Get starting point coordinates
        X0 = float(str(self.pluginGui.lineEdit_vertexX0.text()))
        Y0 = float(str(self.pluginGui.lineEdit_vertexY0.text()))
        Z0 = float(str(self.pluginGui.lineEdit_vertexZ0.text()))

        #check if the starting point is specified
        if (X0 == 0 and Y0 == 0 and Z0 == 90):
            self.say("You must supply a starting point.")
            return 0
        
        # Check if there are any segments
        if (self.pluginGui.table_segmentList.rowCount() < 1):
            self.say("You must enter at least one segment.")
            return 0

        vlist=[]
        vlist.append([X0,Y0,Z0])
        #convert segment list to set of vertice
        for i in range(self.pluginGui.table_segmentList.rowCount()):
            az=str(self.pluginGui.table_segmentList.item(i,0).text())
            dis=float(str(self.pluginGui.table_segmentList.item(i,1).text()))
            zen=str(self.pluginGui.table_segmentList.item(i,2).text())

            if (self.pluginGui.radioButton_englishUnits.isChecked()):
                # adjust for input in feet, not meters
                dis = float(dis)/3.281

            #checking degree input
            if (self.pluginGui.radioButton_azimuthAngle.isChecked()):
                az=float(self.dmsToDd(az))
                zen=float(self.dmsToDd(zen))
            elif (self.pluginGui.radioButton_bearingAngle.isChecked()):
                az=float(self.bearingToDd(az))
                zen=float(self.bearingToDd(zen))

            #correct for magnetic compass headings if necessary
            if (self.pluginGui.radioButton_defaultNorth.isChecked()):
                self.magDev = 0.0
            elif (self.pluginGui.radioButton_magNorth.isChecked()):
                self.magDev = float(self.dmsToDd(str(self.pluginGui.lineEdit_magNorth.text())))
            az = float(az) + float(self.magDev)

            #correct for angles outside of 0.0-360.0
            while (az > 360.0):
                az = az - 360.0
            while (az < 0.0):
                az = az + 360.0

            #checking survey type
            if (self.pluginGui.radioButton_radialSurvey.isChecked()):
                vlist.append(self.nextvertex(vlist[0],dis,az,zen))      #reference first vertex
                surveytype='radial'
            elif (self.pluginGui.radioButton_boundarySurvey.isChecked()):
                vlist.append(self.nextvertex(vlist[-1],dis,az,zen))     #reference previous vertex
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
            elif (surveytype=='radial'):
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
        provider.addFeatures(featurelist)
        if not self.useactivelayer:
            QgsMapLayerRegistry.instance().addMapLayer(vectorlayer)

        self.iface.mapCanvas().refresh()

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
        #dms=dms.replace(" ", "")
        for c in dms:
            if ((not c.isdigit()) and (c != '.') and (c != '-')):
                dms=dms.replace(c,';')
        while (dms.find(";;")>=0):
            dms=dms.replace(";;",';')
        if dms[0]==';':
            dms=dms[1:]
        dms=dms.split(";")
        dd=0
        #dd=str(float(dms[0])+float(dms[1])/60+float(dms[2])/3600)
        for i, f in enumerate(dms):
            if f!="":
                dd+=float(f)/pow(60, i)
        return dd

    def clearList(self):
        self.pluginGui.table_segmentList.clearContents()
        self.pluginGui.table_segmentList.setSortingEnabled(False)
        self.pluginGui.table_segmentList.setRowCount(0)
        self.pluginGui.table_segmentList.setCurrentCell(0, 0) # substitute for missing setCurrentRow()
        #retranslateUi

    def newVertex(self):
        #adds a vertex from the gui
        self.addrow(self.pluginGui.lineEdit_nextAzimuth.text(),
                        self.pluginGui.lineEdit_nextDistance.text(),
                        self.pluginGui.lineEdit_nextVertical.text())

    def addRow(self):
        # this and following must be split to handle both GUI & FILE inputs
        az = self.pluginGui.lineEdit_nextAzimuth.text()
        dist = self.pluginGui.lineEdit_nextDistance.text()
        zen = self.pluginGui.lineEdit_nextVertical.text()
        self.addrow(az, dist, zen)

    def addrow(self,  az=0,  dist=0,  zen = 90):
        #add the vertext to the end of the table
        i=self.pluginGui.table_segmentList.rowCount()
        self.pluginGui.table_segmentList.insertRow(i)
        self.pluginGui.table_segmentList.setItem(i, 0, QTableWidgetItem(str(az).upper()))
        self.pluginGui.table_segmentList.setItem(i, 1, QTableWidgetItem(str(dist)))
        self.pluginGui.table_segmentList.setItem(i, 2, QTableWidgetItem(str(zen)))

    def insertRow(self):
        az = self.pluginGui.lineEdit_nextAzimuth.text()
        dist = self.pluginGui.lineEdit_nextDistance.text()
        zen = self.pluginGui.lineEdit_nextVertical.text()

        #insert the vertext into the table at the current position
        i=self.pluginGui.table_segmentList.currentRow()
        self.pluginGui.table_segmentList.insertRow(i)
        self.pluginGui.table_segmentList.setItem(i, 0, QTableWidgetItem(str(az).upper()))
        self.pluginGui.table_segmentList.setItem(i, 1, QTableWidgetItem(str(dist)))
        self.pluginGui.table_segmentList.setItem(i, 2, QTableWidgetItem(str(zen)))

    def delRow(self):
        self.pluginGui.table_segmentList.removeRow(self.pluginGui.table_segmentList.currentRow())

    def moveup(self):
        pass

    def movedown(self):
        pass

    def startgetpoint(self):
        #point capture tool
        self.tool.finished.connect(self.getpoint)
        self.saveTool = self.canvas.mapTool()
        self.canvas.setMapTool(self.tool)

    def getpoint(self,pt):
        self.pluginGui.lineEdit_vertexX0.setText(str(pt.x()))
        self.pluginGui.lineEdit_vertexY0.setText(str(pt.y()))
        self.canvas.setMapTool(self.saveTool)
        self.tool.finished.disconnect(self.getpoint)

    def reproject(self, vlist,  vectorlayer):
        renderer=self.canvas.mapRenderer()
        for i, point in enumerate(vlist):
            vlist[i]= renderer.layerToMapCoordinates(vectorlayer, QgsPoint(point[0], point[1]))
        return vlist

    def setAngle(self, s):
        #self.say('processing angleType='+s)
        if (s=='azimuth'):
            self.pluginGui.radioButton_azimuthAngle.setChecked(True)
        elif (s=='bearing'):
            self.pluginGui.radioButton_bearingAngle.setChecked(True)
        elif (s=='polar'):
            self.pluginGui.radioButton_polorCoordAngle.setChecked(True)
        else:
            self.say('invalid angle type: '+s)

    def setHeading(self,  s):
        #self.say('processing headingType='+s)
        if (s=='coordinate_system'):
            self.pluginGui.radioButton_defaultNorth.setChecked(True)
        elif (s=='magnetic'):
            self.pluginGui.radioButton_magNorth.setChecked(True)
        else:
            self.say('invalid heading type: '+s)

    def setDeclination(self,  s):
        #self.say('processing declination='+s)
        self.pluginGui.lineEdit_magNorth.setText(s)
        self.magDev = float(s)

    def setDistanceUnits(self,  s):
         #self.say('processing distance units='+s)
        if (s=='feet'):
            self.pluginGui.radioButton_englishUnits.setChecked(True)
        else:
            self.pluginGui.radioButton_defaultUnits.setChecked(True)

    def setStartAt(self,  s):
        #self.say('processing startAt='+s)
        coords=s.split(';')
        self.pluginGui.lineEdit_vertexX0.setText(coords[0])
        self.pluginGui.lineEdit_vertexY0.setText(coords[1])
        self.pluginGui.lineEdit_vertexZ0.setText(coords[2])

    def setSurvey(self, s):
        #self.say('processing surveyType='+s)
        if (s=='polygonal'):
            self.pluginGui.radioButton_boundarySurvey.setChecked(True)
        elif (s=='radial'):
            self.pluginGui.radioButton_irrSurvey.setChecked(True)
        else:
            self.say('invalid survey type: '+s)

    def say(self, txt):
        # present a message box on screen
        warn=QgsMessageViewer()
        warn.setMessageAsPlainText(txt)
        warn.showMessage()

    def tell(self, txt):
        # write to bottom of Note area at top of screen
        self.notes.appendPlainText(txt)

    # ---------------------------------------------------------------------------------------------------------------------------------
    #               File handling
    # This section deals with saving the user data to disk, and loading it
    #
    # format:
    #   line 1: angle=Azimuth|Bearing|Polar
    #   line 2: heading=Coordinate System|Magnetic
    #   line 3: declination=[- ]x.xxd[ xx.x'] [E|W]
    #   line 4: distunits=Default|Feet
    #   line 5: startAt=xxxxx.xxxxx, xxxxxx.xxxxx
    #   line 6: survey=Polygonal|Radial
    #   line 7: [data]
    #   line 8 through end: Azimuth; dist; zen
    #
    #       note: lines 1 through 5 are optional if hand entered, but will always be generated when 'saved'
    # ---------------------------------------------------------------------------------------------------------------------------------
    def loadList(self):
        self.fileName=QFileDialog.getOpenFileName(None,"Load data separated by ';'",self.fPath,"")
        if not os.path.exists(self.fileName):
            return 0
        # update selected file's folder
        fInfo = QFileInfo(self.fileName)
        self.fPath = fInfo.absolutePath ()
        self.saveConf()

        # get saved data
        try:
            f=open(self.fileName)
            lines=f.readlines()
            f.close()
            self.clearList()
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
                    elif (parts[0].lower()=='dist_units'):
                        self.setDistanceUnits(parts[1].lower())
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
        except:
            self.say("Invalid input")

    def saveList(self):
        #file=QFileDialog.getSaveFileName(None,"Save segment list to file.",self.fPath,"")
        #self.tell("loaded file name: " + self.fileName)
        file=QFileDialog.getSaveFileName(None,"Save segment list to file.",self.fileName,"")
        if (file == ''): return
        #self.tell('target file: '+file)
        f=open(file, 'w')
        # update selected file's folder
        fInfo = QFileInfo(file)
        self.fPath = fInfo.absolutePath ()
        self.saveConf()

        if (self.pluginGui.radioButton_azimuthAngle.isChecked()):
            s='Azimuth'
        elif (self.pluginGui.radioButton_bearingAngle.isChecked()):
            s='Bearing'
        f.write('angle='+s+'\n')

        if (self.pluginGui.radioButton_defaultNorth.isChecked()):
            s='Coordinate_System'
        elif (self.pluginGui.radioButton_magNorth.isChecked()):
            s='Magnetic'
        f.write('heading='+s+'\n')

        if (self.magDev!=0.0):
            f.write('declination='+str(self.magDev)+'\n')

        if (self.pluginGui.radioButton_defaultUnits.isChecked()):
            s='Default'
        elif (self.pluginGui.radioButton_englishUnits.isChecked()):
            s='Feet'
        f.write('dist_units='+s+'\n')

        f.write('startAt='+str(self.pluginGui.lineEdit_vertexX0.text())+';'+
                                    str(self.pluginGui.lineEdit_vertexY0.text())+';'+
                                    str(self.pluginGui.lineEdit_vertexZ0.text())+'\n')

        if (self.pluginGui.radioButton_boundarySurvey.isChecked()):
            s='Polygonal'
        elif (self.pluginGui.radioButton_radialSurvey.isChecked()):
            s='Radial'
        f.write('survey='+s+'\n')

        f.write('[data]\n')
        for i in range(self.pluginGui.table_segmentList.rowCount()):
            line = str(self.pluginGui.table_segmentList.item(i, 0).text()) +';' \
                    +str(self.pluginGui.table_segmentList.item(i, 1).text()) +';' \
                    +str(self.pluginGui.table_segmentList.item(i, 2).text())
            f.write(line+'\n')

        f.close()

    #------------------------
    def loadConf(self):
        settings=QSettings()
        size = settings.value('/Plugin-qgsAzimuth/size', QSize(800, 600), type=QSize)
        self.pluginGui.resize(size)
        position = settings.value('/Plugin-qgsAzimuth/position', QPoint(0, 0), type=QPoint)
        self.pluginGui.move(position)
        #settings.restoreGeometry(settings.value("Geometry"), QByteArray(), type=QByteArray)
        self.fPath = settings.value('/Plugin-qgsAzimuth/inp_exp_dir', "", type=unicode)
        self.fileName = self.fPath

    def saveConf(self):
        settings=QSettings()
        #settings.setValue("Geometry", self.saveGeometry())
        settings.setValue('/Plugin-qgsAzimuth/size',  self.pluginGui.size())
        settings.setValue('/Plugin-qgsAzimuth/position',  self.pluginGui.pos())
        settings.setValue('/Plugin-qgsAzimuth/inp_exp_dir', self.fPath)

    def sortedDict(self, adict):
        keys = adict.keys()
        keys.sort()
        return map(adict.get, keys)

