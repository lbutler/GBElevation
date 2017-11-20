# -*- coding: utf-8 -*-
"""
 GBElevation - QGIS Plugin
 *************************
 Copyright (c) 2017 Luke Butler (luke@matrado.ca) - Matrado Limited
 Licence - github.com/lbutler/GBElevation/blob/master/LICENSE
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
