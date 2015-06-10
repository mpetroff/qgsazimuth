from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import QCursor, QPixmap
from qgis.core import QGis, QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper, QgsVertexMarker


class LineTool(QgsMapTool):
    """
    A basic point tool that can be connected to actions in order to handle
    point based actions.
    """
    geometryComplete = pyqtSignal(object)
    locationChanged = pyqtSignal(object)

    def __init__(self, canvas):
        super(LineTool, self).__init__(canvas)
        self.m1 = None
        self.m2 = None
        self.p1 = None
        self.p2 = None

        self.snapper = QgsMapCanvasSnapper(self.canvas())
        self.band = QgsRubberBand(canvas, QGis.Line)
        self.band.setWidth(3)
        self.band.setColor(Qt.red)
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                       "      c None",
                                       ".     c #FF0000",
                                       "+     c #FFFFFF",
                                       "                ",
                                       "       +.+      ",
                                       "      ++.++     ",
                                       "     +.....+    ",
                                       "    +.     .+   ",
                                       "   +.   .   .+  ",
                                       "  +.    .    .+ ",
                                       " ++.    .    .++",
                                       " ... ...+... ...",
                                       " ++.    .    .++",
                                       "  +.    .    .+ ",
                                       "   +.   .   .+  ",
                                       "   ++.     .+   ",
                                       "    ++.....+    ",
                                       "      ++.++     ",
                                       "       +.+      "]))

    def canvasReleaseEvent(self, event):
        if self.m2 and self.m1:
            self.reset()

        point = self.snappoint(event.pos())

        if not self.m1:
            self.m1 = QgsVertexMarker(self.canvas())
            self.m1.setIconType(1)
            self.m1.setColor(Qt.blue)
            self.m1.setIconSize(12)
            self.m1.setPenWidth(3)
            self.m1.setCenter(point)
            self.p1 = point
            return

        if not self.m2:
            self.m2 = QgsVertexMarker(self.canvas())
            self.m2.setIconType(1)
            self.m2.setColor(Qt.red)
            self.m2.setIconSize(12)
            self.m2.setPenWidth(3)
            self.m2.setCenter(point)
            self.p2 = point

        if self.m2 and self.m1:
            geom = QgsGeometry.fromPolyline([self.p1, self.p2])
            self.band.setToGeometry(geom, None)
            self.geometryComplete.emit(geom)

    def canvasMoveEvent(self,event):
        point = self.snappoint(event.pos())
        self.locationChanged.emit(point)

    def snappoint(self, point):
        if QGis.QGIS_VERSION_INT >= 20800:
            # Snapping changed in 2.8 and now we do it this way.
            utils = self.canvas().snappingUtils()
            match = utils.snapToMap(point)
            if match.isValid():
                return match.point()
            else:
                return self.canvas().getCoordinateTransform().toMapCoordinates(point)
        else:
            try:
                _, results = self.snapper.snapToBackgroundLayers(point)
                point = results[0].snappedVertex
                return point
            except IndexError:
                return self.canvas().getCoordinateTransform().toMapCoordinates(point)

    def activate(self):
        self.canvas().setCursor(self.cursor)
        self.reset()

    def deactivate(self):
        """
        Deactive the tool.
        """
        pass

    def reset(self):
        self.band.reset()
        self.canvas().scene().removeItem(self.m1)
        self.canvas().scene().removeItem(self.m2)
        self.m1 = None
        self.m2 = None
        self.p1 = None
        self.p2 = None

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return False
