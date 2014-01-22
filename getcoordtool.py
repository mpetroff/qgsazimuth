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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# Raster File Info Tool class
class GetCoordTool(QgsMapTool):
  def __init__(self, canvas):
    QgsMapTool.__init__(self,canvas)
    self.canvas=canvas
    self.cursor = QCursor(QPixmap(["16 16 3 1",
                                   "# c None","a c #000000",". c #ffffff",
                                   ".###########..##",
                                   "...########.aa.#",
                                   ".aa..######.aa.#",
                                   "#.aaa..#####..##",
                                   "#.aaaaa..##.aa.#",
                                   "##.aaaaaa...aa.#",
                                   "##.aaaaaa...aa.#",
                                   "##.aaaaa.##.aa.#",
                                   "###.aaaaa.#.aa.#",
                                   "###.aa.aaa..aa.#",
                                   "####..#..aa.aa.#",
                                   "####.####.aa.a.#",
                                   "##########.aa..#",
                                   "###########.aa..",
                                   "############.a.#",
                                   "#############.##"]), 0, 0)
  
  finished = pyqtSignal(QgsPoint)
  def canvasPressEvent(self,event):
    pixels=event.pos()
    
    snapper=QgsMapCanvasSnapper(self.canvas)
    snapped=snapper.snapToBackgroundLayers(pixels)
    #QMessageBox.information(None,"Teste", str(snapped[1]))
    if len(snapped[1])>0:
        xy=snapped[1][0].snappedVertex
    else:
        #transforming pixels to x,y
        transform = self.canvas.getCoordinateTransform()
        xy = transform.toMapCoordinates(pixels) #captures the clicked coordinate and transform
    self.finished.emit(xy)
  
  def canvasMoveEvent(self,event):
    pass
  
  def canvasReleaseEvent(self,event):
    pass
            
  def activate(self):
    QgsMapTool.activate(self)
    self.canvas.setCursor(self.cursor)
  
  def deactivate(self):
    #QgsMapTool.deactivate(self)
    pass
  
  def isZoomTool(self):
    return False

