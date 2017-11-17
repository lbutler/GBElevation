# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry, QgsRectangle

from GBElevation.models import *

class OSGroundGridCalculatorIDW(OsGroundGridCalculator):

    def __init__(self, gridLayer, gridInterval, power):

        self.power = power

        OsGroundGridCalculator.__init__(self, gridLayer, gridInterval)

    def _useAlgorithm(self, x, y):

        feat = QgsGeometry().fromPoint( QgsPoint(x, y ) )

        values = []
        distances = []
        
        request = QgsFeatureRequest()
        request.setFilterFids(self._getClosestNodeFeatureIds(x,y))

        nearestFourGridNodes = self.gridLayer.getFeatures( request )
        for gridNode in nearestFourGridNodes:
            values.append( gridNode.attribute("HEIGHT") )
            distances.append( gridNode.geometry().distance(feat) )           

        return self._inverseDistanceWeighted(values, distances)

    def _inverseDistanceWeighted(self, values, distances):

        top = 0
        bottom = 0
        for value, distance in zip(values, distances):
            top += value/(distance**self.power)
            bottom +=  1/(distance**self.power)

        return top/bottom
