# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GBElevation
                                 A QGIS plugin
 Calculate elevation of points from 10m & 50m OS NTF files
                              -------------------
        begin                : 2017-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luke Butler - Matrado Limited
        email                : luke@matrado.ca
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry, QgsRectangle

from GBElevation.models import *

class OSGroundGridCalculatorBilinear(OsGroundGridCalculator):

    def __init__(self, gridLayer, gridInterval):

        OsGroundGridCalculator.__init__(self, gridLayer, gridInterval)

    def _useAlgorithm(self, x, y):

        featureIds = self._getClosestNodeFeatureIds(x,y)
        values = {featureId: {'height': self.featuresHeights[0][featureId-1] } for featureId in featureIds}

        request = QgsFeatureRequest()
        request.setFilterFids(featureIds)
        nearestFourGridNodes = self.gridLayer.getFeatures( request )

        for gridNode in nearestFourGridNodes:
            values[gridNode.id()]['geometry'] = gridNode.geometry().asPoint()

        return self._bilinearInterpolation(x, y, values)


    def _bilinearInterpolation(self, x, y, nodes ):

        result = 0

        for nodeId in nodes:

            width = self.gridInterval -  abs(nodes[nodeId]["geometry"].x() - x)
            height = self.gridInterval - abs(nodes[nodeId]["geometry"].y() - y)

            area = (width * height ) / self.gridInterval ** 2
            result += area * nodes[nodeId]["height"]

        return result
