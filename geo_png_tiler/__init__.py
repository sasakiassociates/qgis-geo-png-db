# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoPngTiler
                                 A QGIS plugin
 Export tile rasters in GeoPNG format
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-02-19
        copyright            : (C) 2020 by Sasaki
        email                : kgoulding@sasaki.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GeoPngTiler class from file GeoPngTiler.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geo_png_tiler import GeoPngTiler
    return GeoPngTiler(iface)
