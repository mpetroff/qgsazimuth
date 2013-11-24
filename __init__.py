"""
Copyright (C) 2008-2009 Mauricio Carvalho Mathias de Paulo
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgsAzimuth import qgsazimuth

def classFactory(iface):
  return qgsazimuth(iface)
