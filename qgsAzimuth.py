# ---------------------------------------------------------------------
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
# ---------------------------------------------------------------------

import math
import os

from qgis.PyQt.QtCore import Qt, QFileInfo, QSettings, QSize, QPoint, QCoreApplication
from qgis.PyQt.QtWidgets import QAction, QTableWidgetItem, QFileDialog
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.core import *

from .ui_control import Dock
from . import resources_rc
from math import *
from .getcoordtool import *
from .maptool import LineTool

from . import utils


class qgsazimuth(object):
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
        self.canvas = iface.mapCanvas()
        self.fPath = (
            ""
        )  # set default working directory, updated from config file & by Import/Export
        self.bands = []

    def log(self, message):
        QgsMessageLog.logMessage(str(message), "Plugin")
        self.iface.messageBar().pushCritical("Error", str(message))

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(
            QIcon(":icons/qgsazimuth.png"),
            "Azimuth and distance",
            self.iface.mainWindow(),
        )
        self.action.setWhatsThis("Azimuth and distance")
        self.action.triggered.connect(self.run)

        self.bandpoint = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.bandpoint.setIcon(QgsRubberBand.ICON_CROSS)
        self.bandpoint.setColor(QColor.fromRgb(255, 50, 255))
        self.bandpoint.setWidth(3)
        self.bandpoint.setIconSize(20)

        # add toolbar button and menu item
        self.iface.addPluginToMenu("&Topography", self.action)
        self.iface.addToolBarIcon(self.action)

        self.dock = Dock(self.iface.mainWindow())
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        self.dock.hide()
        self.pluginGui = self.dock.widget()

        self.dock.closed.connect(self.cleanup)
        self.pluginGui.pushButton_vertexAdd.clicked.connect(self.addRow)
        self.pluginGui.pushButton_vertexInsert.clicked.connect(self.insertRow)
        self.pluginGui.pushButton_segListRowDel.clicked.connect(self.delRow)
        self.pluginGui.pushButton_segListLoad.clicked.connect(self.loadList)
        self.pluginGui.pushButton_segListClear.clicked.connect(self.clearList)
        self.pluginGui.pushButton_objectDraw.clicked.connect(self.addgeometry)
        self.pluginGui.pushButton_startCapture.clicked.connect(self.startgetpoint)
        self.pluginGui.pushButton_segListSave.clicked.connect(self.saveList)
        self.pluginGui.pushButton_useLast.clicked.connect(self.use_last_vertex)

        self.pluginGui.pickAngle1_button.clicked.connect(self.select_angle1)
        self.pluginGui.pickAngle2_button.clicked.connect(self.select_angle2)
        self.pluginGui.clearMarkers_button.clicked.connect(self.clear_markers)
        self.pluginGui.copyDiff_button.clicked.connect(self.copy_diff_offset)

        # self.pluginGui.table_segmentList.cellChanged.connect(self.render_temp_band)

        self.pluginGui.table_segmentList.setCurrentCell(0, 0)

        self.tool = GetCoordTool(self.canvas)
        self.tool.finished.connect(self.getpoint)
        self.tool.locationChanged.connect(self.pluginGui.update_startpoint)
        self.tool.locationChanged.connect(self.update_marker_location)

        self.angletool = LineTool(self.canvas)
        self.angletool.geometryComplete.connect(self.update_angle1)
        self.angletool.locationChanged.connect(self.update_marker_location)

        self.angletool2 = LineTool(self.canvas)
        self.angletool2.geometryComplete.connect(self.update_angle2)
        self.angletool2.locationChanged.connect(self.update_marker_location)

        self.pluginGui.azimuth1_edit.textChanged.connect(self.update_angle_calc)
        self.pluginGui.azimuth2_edit.textChanged.connect(self.update_angle_calc)

        self.pluginGui.lineEdit_magNorth.textChanged.connect(self.update_offsetlabel)
        self.pluginGui.radioButton_defaultNorth.toggled.connect(self.update_offsetlabel)

        self.pluginGui.radioButton_azimuthAngle.toggled.connect(self.update_angle_label)
        self.pluginGui.radioButton_bearingAngle.toggled.connect(self.update_angle_label)

    def update_offsetlabel(self, *args):
        mag = self.mag_dev
        self.pluginGui.offsetLabel.setText(str(mag))

    def update_angle_label(self, *args):
        if self.angletype == "azimuth":
            item = self.pluginGui.table_segmentList.horizontalHeaderItem(0)
            item.setText(QCoreApplication.translate("Form", "Azimuth"))
            self.pluginGui.label_angle.setText(
                QCoreApplication.translate("Form", "Azimuth:")
            )
        else:
            item = self.pluginGui.table_segmentList.horizontalHeaderItem(0)
            item.setText(QCoreApplication.translate("Form", "Bearing"))
            self.pluginGui.label_angle.setText(
                QCoreApplication.translate("Form", "Bearing:")
            )

    def copy_diff_offset(self):
        diff = self.pluginGui.azimuthDiff_edit.text()
        self.pluginGui.lineEdit_magNorth.setText(diff)

    def clear_markers(self):
        self.angletool2.reset()
        self.angletool.reset()
        self.pluginGui.azimuth1_edit.setText(str(0))
        self.pluginGui.azimuth2_edit.setText(str(0))

    def update_angle_calc(self):
        a1 = self.pluginGui.azimuth1_edit.text()
        a2 = self.pluginGui.azimuth2_edit.text()
        a1 = utils.dmsToDd(a1)
        a2 = utils.dmsToDd(a2)
        try:
            a1 = float(a1)
            a2 = float(a2)
        except ValueError:
            self.pluginGui.azimuthDiff_edit.setText("")
            return

        diff = a2 - a1
        self.pluginGui.azimuthDiff_edit.setText(str(diff))

    def select_angle1(self):
        self.canvas.setMapTool(self.angletool)

    def update_angle1(self, geometry):
        az = utils.azimuth_from_line(geometry)
        az = str(az)
        self.pluginGui.azimuth1_edit.setText(az)

    def update_angle2(self, geometry):
        az = utils.azimuth_from_line(geometry)
        az = str(az)
        self.pluginGui.azimuth2_edit.setText(az)

    def select_angle2(self):
        self.canvas.setMapTool(self.angletool2)

    def update_marker_location(self, point):
        self.bandpoint.setToGeometry(QgsGeometry.fromPointXY(point), None)

    def unload(self):
        # remove the plugin menu item and icon
        self.saveConf()
        self.iface.removeDockWidget(self.dock)
        self.iface.removePluginMenu("&Topography", self.action)
        self.iface.removeToolBarIcon(self.action)
        self.bandpoint.reset()
        self.tool.cleanup()
        self.clear_markers()
        del self.angletool2
        del self.angletool
        del self.tool
        del self.bandpoint

    def run(self):
        # misc init
        self.loadConf()  # get config data
        self.clearList()
        self.setStartAt("0;0;90")  # remove previous StartAt point

        self.pluginGui.lineEdit_crs.setText(
            self.iface.mapCanvas().mapSettings().destinationCrs().description()
        )

        if self.iface.activeLayer():
            self.updatelayertext(self.iface.activeLayer())
            self.pluginGui.radioButton_useActiveLayer.setChecked(True)
        else:
            self.pluginGui.radioButton_useActiveLayer.setEnabled(False)
            self.pluginGui.radioButton_useMemoryLayer.setChecked(True)
        self.iface.currentLayerChanged.connect(self.updatelayertext)
        if not self.dock.isVisible():
            self.dock.show()

        # for debugging convenience
        self.notes = self.pluginGui.plainTextEdit_note

    def cleanup(self):
        self.tool.cleanup()
        self.clear_bands()
        self.saveConf()

    def updatelayertext(self, layer):
        if not layer:
            self.pluginGui.radioButton_useActiveLayer.setEnabled(False)
        else:
            self.pluginGui.radioButton_useActiveLayer.setEnabled(True)
            self.pluginGui.radioButton_useActiveLayer.setText(
                "Active Layer ({0})".format(layer.name())
            )

    @property
    def useactivelayer(self):
        return self.pluginGui.radioButton_useActiveLayer.isChecked()

    def render_temp_band(self, *args):
        """
        Render a temp rubber band for showing the user the results
        """

        self.clear_bands()

        featurelist, vectorlayer = self.create_feature()
        if not featurelist or not vectorlayer:
            return

        for feature in featurelist:
            band = QgsRubberBand(self.iface.mapCanvas())
            if hasattr(band, "setLineStyle"):
                band.setLineStyle(Qt.DotLine)
            band.setWidth(4)
            band.setColor(Qt.darkMagenta)
            band.setToGeometry(feature.geometry(), vectorlayer)
            band.show()
            self.bands.append(band)
        pass

    @property
    def should_open_form(self):
        return self.pluginGui.checkBox_openForm.isChecked()

    @should_open_form.setter
    def should_open_form(self, value):
        return self.pluginGui.checkBox_openForm.setChecked(value)

    def addgeometry(self):
        featurelist, vectorlayer = self.create_feature()
        if not featurelist or not vectorlayer:
            return

        if vectorlayer.sourceCrs().isGeographic():
            self.log(
                "Selected layer uses a geographic CRS, i.e., uses lat/lon "
                "coordinates, but only projected CRSes are supported by plugin!"
            )
            return

        if not self.useactivelayer:
            QgsProject.instance().addMapLayer(vectorlayer)

        vectorlayer.startEditing()
        for feature in featurelist:
            if self.should_open_form:
                form = self.iface.getFeatureForm(vectorlayer, feature)
                form.setMode(QgsAttributeEditorContext.AddFeatureMode)
                if not form.exec_():
                    continue
            else:
                print(feature.isValid())
                print(feature.geometry().asWkt())
                result = vectorlayer.addFeature(feature)
                print("Error adding feature", feature)
                if result == False:
                    self.log("Error in adding feature")

        self.iface.mapCanvas().refresh()
        self.clear_bands()

    def clear_bands(self):
        for band in self.bands:
            band.reset()
        self.bands = []

    def update_draw_button_state(self):
        x, y, z = self.starting_point()
        enabled = True
        if (x == 0 and y == 0 and z == 90) or (
            self.pluginGui.table_segmentList.rowCount() == 0
        ):
            enabled = False
        self.pluginGui.pushButton_objectDraw.setEnabled(enabled)

    def starting_point(self):
        # Get starting point coordinates
        X = float(str(self.pluginGui.lineEdit_vertexX0.text()))
        Y = float(str(self.pluginGui.lineEdit_vertexY0.text()))
        Z = float(str(self.pluginGui.lineEdit_vertexZ0.text()))
        return X, Y, Z

    @property
    def angletype(self):
        if self.pluginGui.radioButton_azimuthAngle.isChecked():
            return "azimuth"
        elif self.pluginGui.radioButton_bearingAngle.isChecked():
            return "bearing"
        elif self.pluginGui.radioButton_polarCoordAngle.isChecked():
            return "polor"

    @angletype.setter
    def angletype(self, value):
        if value == "azimuth":
            self.pluginGui.radioButton_azimuthAngle.setChecked(True)
        elif value == "bearing":
            self.pluginGui.radioButton_bearingAngle.setChecked(True)
        elif value == "polor":
            self.pluginGui.radioButton_polarCoordAngle.setChecked(True)
        else:
            self.pluginGui.radioButton_azimuthAngle.setChecked(True)

    @property
    def distanceunits(self):
        return self.pluginGui.comboBox_distanceUnits.currentText()

    def lower_nospace_compare(self, valueA, valueB):
        """
        Determine if string values match, ignoring
        spacing and capitalization.
        """
        valueA = valueA.replace(" ", "").lower()
        valueB = valueB.replace(" ", "").lower()
        return valueA == valueB

    def get_distanceunit_combobox(self, value):
        """
        Get matching comboBox_distanceUnits item, ignoring
        spacing and capitalization. If not found, assume Default (0).
        """
        items = self.pluginGui.comboBox_distanceUnits
        for itemNumber in range(items.count()):
            if self.lower_nospace_compare(items.itemText(itemNumber), value):
                return itemNumber
        return 0

    @distanceunits.setter
    def distanceunits(self, value):
        value = self.get_distanceunit_combobox(value)
        self.pluginGui.comboBox_distanceUnits.setCurrentIndex(value)

    @property
    def angleunit(self):
        if self.pluginGui.radioButton_degreeUnit.isChecked():
            return "degree"
        elif self.pluginGui.radioButton_gradianUnit.isChecked():
            return "gradian"

    @angleunit.setter
    def angleunit(self, value):
        if value == "degree":
            self.pluginGui.radioButton_degreeUnit.setChecked(True)
        elif value == "gradian":
            self.pluginGui.radioButton_gradianUnit.setChecked(True)
        else:
            self.pluginGui.radioButton_degreeUnit.setChecked(True)

    @property
    def northtype(self):
        if self.pluginGui.radioButton_magNorth.isChecked():
            return "magnetic"
        else:
            return "default"

    @northtype.setter
    def northtype(self, value):
        if value == "magnetic":
            self.pluginGui.radioButton_magNorth.setChecked(True)
        else:
            self.pluginGui.radioButton_defaultNorth.setChecked(True)

    @property
    def mag_dev(self):
        if self.pluginGui.radioButton_magNorth.isChecked():
            value = str(self.pluginGui.lineEdit_magNorth.text())
            try:
                return float(value)
            except ValueError:
                try:
                    if self.pluginGui.radioButton_gradianUnit.isChecked():
                        value = utils.gradianToDd(value)
                    return float(utils.dmsToDd(value))
                except IndexError:
                    return 0.0
        elif self.pluginGui.radioButton_defaultNorth.isChecked():
            return 0.0
        else:
            return 0.0

    @mag_dev.setter
    def mag_dev(self, value):
        self.pluginGui.lineEdit_magNorth.setText(str(value))

    @property
    def surveytype(self):
        if self.pluginGui.radioButton_radialSurvey.isChecked():
            surveytype = "radial"
        elif self.pluginGui.radioButton_boundarySurvey.isChecked():
            surveytype = "polygonal"
        return surveytype

    @surveytype.setter
    def surveytype(self, value):
        if value == "radial":
            self.pluginGui.radioButton_radialSurvey.setChecked(True)
        elif value == "polygonal":
            self.pluginGui.radioButton_boundarySurvey.setChecked(True)
        else:
            self.pluginGui.radioButton_boundarySurvey.setChecked(True)

    def use_last_vertex(self):
        # Get the last point from the last band
        x, y, z = 0, 0, 90
        arcpoint_count = self.arc_count
        points = self.get_points(self.surveytype, arcpoint_count)
        try:
            point = points[-1]
            x, y, z = point.x, point.y, point.z
        except IndexError:
            # Don't do anything if there is no last point
            return

        point = QgsPointXY(x, y)
        self.pluginGui.update_startpoint(point, z)
        self.update_marker_location(point)
        self.clearList()

    def table_entries(self):
        """
        Return the entries for each row in the table
        """
        rows = self.pluginGui.table_segmentList.rowCount()
        for row in range(rows):
            az = self.pluginGui.table_segmentList.item(row, 0).text()
            dis = float(str(self.pluginGui.table_segmentList.item(row, 1).text()))
            zen = self.pluginGui.table_segmentList.item(row, 2).text()
            direction = self.pluginGui.table_segmentList.item(row, 4).text()
            direction = utils.Direction.resolve(direction)

            try:
                radius = float(self.pluginGui.table_segmentList.item(row, 3).text())
            except ValueError:
                radius = None

            yield az, dis, zen, direction, radius

    def get_distanceunit_enum(self, value):
        """
        Get matching distanceunit enum item, ignoring
        spacing and capitalization.
        """
        items = QgsUnitTypes.DistanceUnit
        if 'Degrees' in dir(items) or 'DistanceDegrees' in dir(items):
            items = list(items)
            for item in items:
                if self.lower_nospace_compare(item.name, value) or self.lower_nospace_compare(item.name, "distance" + value):
                    return item
        else:
            items = dir(QgsUnitTypes)
            for item in items:
                itemObject = getattr(QgsUnitTypes, item)
                if isinstance(itemObject, QgsUnitTypes.DistanceUnit):
                    if self.lower_nospace_compare(item, "distance" + value):
                        return itemObject
        return -1
    
    def get_distanceunits_factor(self, fromUnits=None, toUnits=None):
        """
        Determine multiplication factor between distanceunits value
        and CRS map units. If cannot calculate, assume Default (1.0).
        """
        if fromUnits is None:
            fromUnits = self.distanceunits
        fromUnits = self.get_distanceunit_enum(fromUnits)
    
        if fromUnits > -1:
            if toUnits is None:
                toUnits = self.drawing_layer.sourceCrs().mapUnits()
            else:
                toUnits = self.get_distanceunit_enum(toUnits)
            if toUnits > -1:
                return QgsUnitTypes.fromUnitToUnitFactor(fromUnits, toUnits)

        return float(1.0)

    def get_points(self, surveytype, arcpoint_count):
        """
        Return a list of calculated points for the full run.
        :param surveytype:
        :return:
        """
        X, Y, Z = self.starting_point()

        if (X == 0 and Y == 0 and Z == 90) or (
            self.pluginGui.table_segmentList.rowCount() == 0
        ):
            return []

        vlist = []
        vlist.append(utils.Point(X, Y, Z))
        # convert segment list to set of vertice
        for az, dis, zen, direction, radius in self.table_entries():
            # adjust for input in non-default units
            dis = float(dis) * self.get_distanceunits_factor()

            # checking degree input
            if self.pluginGui.radioButton_azimuthAngle.isChecked():
                if self.pluginGui.radioButton_gradianUnit.isChecked():
                    az = utils.gradianToDd(az)
                    zen = utils.gradianToDd(zen)
                else:
                    az = float(utils.dmsToDd(az))
                    zen = float(utils.dmsToDd(zen))
            elif self.pluginGui.radioButton_bearingAngle.isChecked():
                az = float(self.bearingToDd(az))
                zen = float(self.bearingToDd(zen))

            # correct for magnetic compass headings if necessary
            self.magDev = self.mag_dev

            az = float(az) + float(self.magDev)

            # correct for angles outside of 0.0-360.0
            while az > 360.0:
                az = az - 360.0

            while az < 0.0:
                az = az + 360.0

            # checking survey type
            if surveytype == "radial":
                reference_point = vlist[0]  # reference first vertex

            if surveytype == "polygonal":
                reference_point = vlist[-1]  # reference previous vertex

            nextpoint = utils.nextvertex(reference_point, dis, az, zen)

            if radius:
                # If there is a radius then we are drawing a arc.
                
                # adjust for input in non-default units
                radius = float(radius) * self.get_distanceunits_factor()

                # Make sure distance <= diameter
                if dis > 2 * radius:
                    self.log("Invalid arc: distance can't be greater than diameter")
                    return []

                # Calculate the arc points.
                points = list(
                    utils.arc_points(
                        reference_point,
                        nextpoint,
                        dis,
                        radius,
                        point_count=arcpoint_count,
                        direction=direction,
                        zenith_angle=zen,
                    )
                )

                if direction == utils.Direction.ANTICLOCKWISE:
                    points = reversed(points)

                # Append them to the final points list.
                vlist.extend(points)

            vlist.append(nextpoint)

        return vlist

    @property
    def drawing_layer(self):
        if self.useactivelayer:
            vectorlayer = self.iface.activeLayer()
        else:
            code = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            vectorlayer = QgsVectorLayer(
                "LineString?crs={}".format(code), "tmp_plot", "memory"
            )
        return vectorlayer

    @property
    def arc_count(self):
        """
        The number of points to use when drawing arcs
        """
        return self.pluginGui.spin_arclines.value()

    @arc_count.setter
    def arc_count(self, value):
        """
        The number of points to use when drawing arcs
        """
        self.pluginGui.spin_arclines.setValue(value)

    def create_feature(self):
        vectorlayer = self.drawing_layer

        # reprojecting to projects SRS
        arcpoint_count = self.arc_count
        points = self.get_points(self.surveytype, arcpoint_count)

        if not points:
            return None, None

        vlist = self.reproject(points, vectorlayer)

        as_segments = self.pluginGui.checkBox_asSegments.isChecked()

        featurelist = []
        geometrytype = vectorlayer.geometryType()
        if geometrytype == QgsWkbTypes.PointGeometry:
            points = utils.to_qgspoints(vlist)
            features = utils.createpoints(points)
            featurelist.extend(features)
        elif geometrytype == QgsWkbTypes.LineGeometry:
            if as_segments:
                # If the line is to be draw as segments then we loop the pairs and create a line for each one.
                points_to_join = []
                in_arc = False
                for pair in utils.pairs(
                    vlist, matchtail=self.surveytype == "polygonal"
                ):
                    start, end = pair[0], pair[1]
                    # If we are not drawing the arc then just add the pair to get a single line
                    if not start.arc_point and not end.arc_point:
                        points_to_join = pair
                    else:
                        # If we are in a arc we need to handle drawing it as one line
                        # which means grabbing each pair until we are finished the arc
                        if not start.arc_point and end.arc_point:
                            points_to_join = []
                            in_arc = True

                        if start.arc_point and not end.arc_point:
                            points_to_join.append(start)
                            points_to_join.append(end)
                            in_arc = False

                        if in_arc:
                            points_to_join.append(start)
                            points_to_join.append(end)
                            continue
                    pointlist = utils.to_qgspoints(
                        points_to_join, repeatfirst=self.surveytype == "radial"
                    )
                    feature = utils.createline(pointlist)
                    featurelist.append(feature)
            else:
                pointlist = utils.to_qgspoints(
                    vlist, repeatfirst=self.surveytype == "radial"
                )
                feature = utils.createline(pointlist)
                featurelist.append(feature)
        elif geometrytype == QgsWkbTypes.PolygonGeometry:
            polygon = utils.to_qgspoints(vlist)
            feature = utils.createpolygon([polygon])
            if feature:
                featurelist.append(feature)

        # Add the fields for the current layer
        for feature in featurelist:
            feature.setFields(vectorlayer.fields())

        return featurelist, vectorlayer

    def bearingToDd(self, dms):
        # allow survey bearings in form:  - N 25d 34' 40" E
        # where minus ('-') sign allows handling bearings given in reverse direction
        dms = dms.strip()
        if dms[0] == "-":
            rev = True
            dms = dms[1:].strip()
        else:
            rev = False

        baseDir = dms[0].upper()
        if baseDir in ["N", "S"]:
            adjDir = dms[-1].upper()
            bearing = True
            if baseDir == "N":
                if adjDir == "E":
                    base = 0.0
                    adj = "add"
                elif adjDir == "W":
                    base = 360.0
                    adj = "sub"
                else:
                    return 0
            elif baseDir == "S":
                base = 180.0
                if adjDir == "E":
                    adj = "sub"
                elif adjDir == "W":
                    adj = "add"
                else:
                    return 0
        else:
            bearing = False

        if self.pluginGui.radioButton_gradianUnit.isChecked():
            dd = utils.gradianToDd(dms)
        else:
            dd = utils.dmsToDd(dms)

        if rev:
            dd = float(dd) + 180.0

        if bearing == True:
            if adj == "add":
                dd = float(base) + float(dd)
            elif adj == "sub":
                dd = float(base) - float(dd)

        return dd

    def clearList(self):
        self.pluginGui.table_segmentList.clearContents()
        self.pluginGui.table_segmentList.setSortingEnabled(False)
        self.pluginGui.table_segmentList.setRowCount(0)
        self.pluginGui.table_segmentList.setCurrentCell(
            0, 0
        )  # substitute for missing setCurrentRow()
        self.render_temp_band()
        # retranslateUi

    def newVertex(self):
        # adds a vertex from the gui
        self.addrow(
            self.pluginGui.lineEdit_nextAzimuth.text(),
            self.pluginGui.lineEdit_nextDistance.value(),
            self.pluginGui.lineEdit_nextVertical.text(),
            self.pluginGui.spin_radius.value(),
        )

    def addRow(self):
        # this and following must be split to handle both GUI & FILE inputs
        az = self.pluginGui.lineEdit_nextAzimuth.text()
        dist = self.pluginGui.lineEdit_nextDistance.value()
        zen = self.pluginGui.lineEdit_nextVertical.text()
        radius = self.pluginGui.spin_radius.value()
        if radius == 0:
            radius = None
            direction = None
        else:
            if self.pluginGui.radio_anticlockwise.isChecked():
                direction = "anticlockwise"
            else:
                direction = "clockwise"
        self.addrow(az, dist, zen, radius, direction)

    def addrow(self, az=0, dist=0, zen=90, radius=None, direction=None):
        # add the vertex to the end of the table
        row = self.pluginGui.table_segmentList.rowCount()
        self.pluginGui.table_segmentList.insertRow(row)
        self.pluginGui.table_segmentList.setItem(
            row, 0, QTableWidgetItem(str(az).upper())
        )
        self.pluginGui.table_segmentList.setItem(row, 1, QTableWidgetItem(str(dist)))
        self.pluginGui.table_segmentList.setItem(row, 2, QTableWidgetItem(str(zen)))
        self.pluginGui.table_segmentList.setItem(row, 3, QTableWidgetItem(str(radius)))
        self.pluginGui.table_segmentList.setItem(
            row, 4, QTableWidgetItem(str(direction))
        )
        self.render_temp_band()

    def insertRow(self):
        az = self.pluginGui.lineEdit_nextAzimuth.text()
        dist = self.pluginGui.lineEdit_nextDistance.value()
        zen = self.pluginGui.lineEdit_nextVertical.text()
        radius = self.pluginGui.spin_radius.value()

        if radius == 0:
            radius = None
            direction = None
        else:
            if self.pluginGui.radio_anticlockwise.isChecked():
                direction = "anticlockwise"
            else:
                direction = "clockwise"

        # insert the vertext into the table at the current position
        row = self.pluginGui.table_segmentList.currentRow()
        self.pluginGui.table_segmentList.insertRow(row)
        self.pluginGui.table_segmentList.setItem(
            row, 0, QTableWidgetItem(str(az).upper())
        )
        self.pluginGui.table_segmentList.setItem(row, 1, QTableWidgetItem(str(dist)))
        self.pluginGui.table_segmentList.setItem(row, 2, QTableWidgetItem(str(zen)))
        self.pluginGui.table_segmentList.setItem(row, 3, QTableWidgetItem(str(radius)))
        self.pluginGui.table_segmentList.setItem(
            row, 4, QTableWidgetItem(str(direction))
        )
        self.render_temp_band()

    def delRow(self):
        self.pluginGui.table_segmentList.removeRow(
            self.pluginGui.table_segmentList.currentRow()
        )
        self.render_temp_band()

    def moveup(self):
        self.render_temp_band()
        pass

    def movedown(self):
        self.render_temp_band()
        pass

    def startgetpoint(self):
        # point capture tool
        self.saveTool = self.canvas.mapTool()
        self.canvas.setMapTool(self.tool)

    def getpoint(self, pt):
        self.clear_markers()
        self.pluginGui.update_startpoint(pt)
        self.canvas.setMapTool(self.saveTool)

    def reproject(self, vlist, vectorlayer):
        renderer = self.canvas.mapSettings()
        for row, point in enumerate(vlist):
            new_point = renderer.layerToMapCoordinates(
                vectorlayer, QgsPointXY(point[0], point[1])
            )
            # Translate it into our new point with arc_point info
            new_point = utils.Point(
                new_point.x(), new_point.y(), arc_point=point.arc_point
            )
            vlist[row] = new_point
        return vlist

    def setAngle(self, s):
        # self.say('processing angleType='+s)
        if s == "azimuth":
            self.pluginGui.radioButton_azimuthAngle.setChecked(True)
        elif s == "bearing":
            self.pluginGui.radioButton_bearingAngle.setChecked(True)
        elif s == "polar":
            self.pluginGui.radioButton_polorCoordAngle.setChecked(True)
        else:
            self.say("invalid angle type: " + s)

    def setHeading(self, s):
        # self.say('processing headingType='+s)
        if s == "coordinate_system":
            self.pluginGui.radioButton_defaultNorth.setChecked(True)
        elif s == "magnetic":
            self.pluginGui.radioButton_magNorth.setChecked(True)
        else:
            self.say("invalid heading type: " + s)

    def setDeclination(self, s):
        # self.say('processing declination='+s)
        self.pluginGui.lineEdit_magNorth.setText(s)
        self.magDev = float(s)

    def setDistanceUnits(self, s):
        # self.say('processing distance units='+s)
        self.distanceunits = s

    def setAngleUnit(self, s):
        if s == "gradian":
            self.pluginGui.radioButton_gradianUnit.setChecked(True)
        else:
            self.pluginGui.radioButton_degreeUnit.setChecked(True)

    def setStartAt(self, s):
        # self.say('processing startAt='+s)
        coords = [float(v) for v in s.split(";")]
        point = QgsPointXY(coords[0], coords[1])
        self.pluginGui.update_startpoint(point, coords[2])

    def setSurvey(self, s):
        # self.say('processing surveyType='+s)
        if s == "polygonal":
            self.pluginGui.radioButton_boundarySurvey.setChecked(True)
        elif s == "radial":
            self.pluginGui.radioButton_radialSurvey.setChecked(True)
        else:
            self.say("invalid survey type: " + s)

    def say(self, txt):
        # present a message box on screen
        warn = QgsMessageViewer()
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
        self.fileName, _ = QFileDialog.getOpenFileName(
            None, "Load data separated by ';'", self.fPath, ""
        )
        if not os.path.exists(self.fileName):
            return 0
        # update selected file's folder
        fInfo = QFileInfo(self.fileName)
        self.fPath = fInfo.absolutePath()
        self.saveConf()

        self.render_temp_band()
        # get saved data
        try:
            f = open(self.fileName)
            lines = f.readlines()
            f.close()
            self.clearList()
            for line in lines:
                # remove trailing 'new lines', etc and break into parts
                parts = ((line.strip()).lower()).split("=")
                if len(parts) > 1:
                    # self.say("line="+line+'\nparts[0]='+parts[0]+'\nparts[1]='+parts[1])
                    if parts[0].lower() == "angle":
                        self.setAngle(parts[1].lower())
                    elif parts[0].lower() == "heading":
                        self.setHeading(parts[1].lower())
                    elif parts[0].lower() == "declination":
                        self.setDeclination(parts[1].lower())
                    elif parts[0].lower() == "dist_units":
                        self.setDistanceUnits(parts[1].lower())
                    elif parts[0].lower() == "angle_unit":
                        self.setAngleUnit(parts[1].lower())
                    elif parts[0].lower() == "startat":
                        self.setStartAt(parts[1].lower())
                    elif parts[0].lower() == "survey":
                        self.setSurvey(parts[1].lower())
                else:
                    coords = tuple((line.strip()).split(";"))
                    if coords[0].lower() == "[data]":
                        pass
                    else:
                        self.addrow(*coords)
        except:
            self.say("Invalid input")

    def saveList(self):
        file, _ = QFileDialog.getSaveFileName(
            None, "Save segment list to file.", self.fileName, ""
        )
        if file == "":
            return
        f = open(file, "w")
        # update selected file's folder
        fInfo = QFileInfo(file)
        self.fPath = fInfo.absolutePath()
        self.saveConf()

        if self.pluginGui.radioButton_azimuthAngle.isChecked():
            s = "Azimuth"
        elif self.pluginGui.radioButton_bearingAngle.isChecked():
            s = "Bearing"
        f.write("angle=" + s + "\n")

        if self.pluginGui.radioButton_defaultNorth.isChecked():
            s = "Coordinate_System"
        elif self.pluginGui.radioButton_magNorth.isChecked():
            s = "Magnetic"
        f.write("heading=" + s + "\n")

        if hasattr(self, "magDev") and self.magDev != 0.0:
            f.write("declination=" + str(self.magDev) + "\n")

        f.write("dist_units=" + self.distanceunits + "\n")

        if self.pluginGui.radioButton_degreeUnit.isChecked():
            s = "degree"
        elif self.pluginGui.radioButton_gradianUnit.isChecked():
            s = "gradian"
        f.write("angle_unit=" + s + "\n")

        f.write(
            "startAt="
            + str(self.pluginGui.lineEdit_vertexX0.text())
            + ";"
            + str(self.pluginGui.lineEdit_vertexY0.text())
            + ";"
            + str(self.pluginGui.lineEdit_vertexZ0.text())
            + "\n"
        )

        if self.pluginGui.radioButton_boundarySurvey.isChecked():
            s = "Polygonal"
        elif self.pluginGui.radioButton_radialSurvey.isChecked():
            s = "Radial"
        f.write("survey=" + s + "\n")

        f.write("[data]\n")
        for row in range(self.pluginGui.table_segmentList.rowCount()):
            line = (
                str(self.pluginGui.table_segmentList.item(row, 0).text())
                + ";"
                + str(self.pluginGui.table_segmentList.item(row, 1).text())
                + ";"
                + str(self.pluginGui.table_segmentList.item(row, 2).text())
                + ";"
                + str(self.pluginGui.table_segmentList.item(row, 3).text())
                + ";"
                + str(self.pluginGui.table_segmentList.item(row, 4).text())
            )
            f.write(line + "\n")

        f.close()

    # ------------------------
    def loadConf(self):
        settings = QSettings()
        size = settings.value("/Plugin-qgsAzimuth/size", QSize(800, 600), type=QSize)
        position = settings.value(
            "/Plugin-qgsAzimuth/position", QPoint(0, 0), type=QPoint
        )
        if position.isNull():
            position = QPoint(0, 0) # QPoint(0, 0) gets cast to NULL
        self.fPath = settings.value("/Plugin-qgsAzimuth/inp_exp_dir", "", type=str)
        self.angletype = settings.value("/Plugin-qgsAzimuth/angletype", "", type=str)

        self.should_open_form = settings.value(
            "/Plugin-qgsAzimuth/open_form", True, type=bool
        )
        self.surverytype = settings.value("/Plugin-qgsAzimuth/type", "", type=str)
        self.northtype = settings.value("/Plugin-qgsAzimuth/northtype", "", type=str)
        self.mag_dev = settings.value(
            "/Plugin-qgsAzimuth/northtype_value", 0.0, type=float
        )
        self.distanceunits = settings.value(
            "/Plugin-qgsAzimuth/distanceunits", "", type=str
        )
        self.angleunit = settings.value("/Plugin-qgsAzimuth/angleunit", "", type=str)
        if self.angleunit == "gradian":
            self.pluginGui.lineEdit_nextVertical.setText("100")
        self.angletype = settings.value("/Plugin-qgsAzimuth/angletype", "", type=str)
        self.arc_count = settings.value("/Plugin-qgsAzimuth/arcpoints", 6, type=int)

        self.pluginGui.resize(size)
        self.pluginGui.move(position)
        self.fileName = self.fPath
        # settings.restoreGeometry(settings.value("Geometry"), QByteArray(), type=QByteArray)

    def saveConf(self):
        settings = QSettings()
        # settings.setValue("Geometry", self.saveGeometry())
        settings.setValue("/Plugin-qgsAzimuth/size", self.pluginGui.size())
        settings.setValue("/Plugin-qgsAzimuth/position", self.pluginGui.pos())
        settings.setValue("/Plugin-qgsAzimuth/inp_exp_dir", self.fPath)
        settings.setValue("/Plugin-qgsAzimuth/open_form", self.should_open_form)
        settings.setValue("/Plugin-qgsAzimuth/type", self.surveytype)
        settings.setValue("/Plugin-qgsAzimuth/northtype", self.northtype)
        settings.setValue("/Plugin-qgsAzimuth/northtype_value", self.mag_dev)
        settings.setValue("/Plugin-qgsAzimuth/distanceunits", self.distanceunits)
        settings.setValue("/Plugin-qgsAzimuth/angleunit", self.angleunit)
        settings.setValue("/Plugin-qgsAzimuth/angletype", self.angletype)
        settings.setValue("/Plugin-qgsAzimuth/arcpoints", self.arc_count)

    def sortedDict(self, adict):
        keys = list(adict.keys())
        keys.sort()
        return list(map(adict.get, keys))
