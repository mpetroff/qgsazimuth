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

def name():
  return "Azimuth and Distance Plugin"

def description():
  return "Creates a polygon from azimuths and distances."

def version():
  return "Version 0.8.3"

def qgisMinimumVersion():
  return "1.0"

def authorName():
  return "Mauricio de Paulo and Fred Laplante"

def classFactory(iface):
  return qgsazimuth(iface)
