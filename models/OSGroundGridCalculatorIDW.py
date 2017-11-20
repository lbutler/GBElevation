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

class OSGroundGridCalculatorIDW(OsGroundGridCalculator):

    def __init__(self, gridLayer, gridInterval, power):

        self.power = power

        OsGroundGridCalculator.__init__(self, gridLayer, gridInterval)

    def _useAlgorithm(self, x, y):

        elevationPoint = QgsGeometry().fromPoint( QgsPoint(x, y ) )

        featureIds = self._getClosestNodeFeatureIds(x,y)
        values = {featureId: {'height': self.featuresHeights[0][featureId-1] } for featureId in featureIds}

        request = QgsFeatureRequest()
        request.setFilterFids(featureIds)
        nearestFourGridNodes = self.gridLayer.getFeatures( request )

        for gridNode in nearestFourGridNodes:
            values[gridNode.id()]['distance'] = gridNode.geometry().distance(elevationPoint)

        return self._inverseDistanceWeighted(values)

    def _inverseDistanceWeighted(self, nodes):

        top = 0
        bottom = 0

        for nodeId in nodes:
            value = nodes[nodeId]["height"]
            distance = nodes[nodeId]["distance"]

            top += value / (distance**self.power)
            bottom +=  1 / (distance**self.power)

        return top/bottom
