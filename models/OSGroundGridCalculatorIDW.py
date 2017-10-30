# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry, QgsRectangle

from GBElevation.models import *

class OSGroundGridCalculatorIDW(OsGroundGridCalculator):

    def __init__(self, gridLayer, gridInterval, power):

        self.power = power

        OsGroundGridCalculator.__init__(self, gridLayer, gridInterval)

    def _useAlgorithm(self, x, y):

        values = []
        distances = []

        feat = QgsGeometry().fromPoint( QgsPoint(x, y) )

        pointTopLeft = QgsPoint(x - self.gridInterval, y + self.gridInterval)
        pointBottomRight  = QgsPoint(x + self.gridInterval, y - self.gridInterval)
        square = QgsRectangle(pointTopLeft, pointBottomRight)

        nearest = self._gridIndex.intersects(square)
        for n in nearest:
            f = self.gridLayer.getFeatures(request=QgsFeatureRequest(n))
            for g in f:
                values.append( g.attribute("HEIGHT") )
                distances.append( g.geometry().distance(feat) )

        return self._inverseDistanceWeighted(values, distances)

    def _inverseDistanceWeighted(self, values, distances):

        top = 0
        bottom = 0
        for value, distance in zip(values, distances):
            top += value/(distance**self.power)
            bottom +=  1/(distance**self.power)

        return top/bottom
