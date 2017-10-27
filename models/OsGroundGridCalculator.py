# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry

class OsGroundGridCalculator:

    def __init__(self, gridLayer, gridInterval):

        self.gridLayer = gridLayer
        self.gridInterval = gridInterval
        self._gridIndex = QgsSpatialIndex( self.gridLayer.getFeatures() )


    def calculateElevation(self, x, y):

        if self._isAtIntersection(x, y):
            return self._getIntersectionElevation(x,y)
        else:
            values = []
            distances = []
            power = 2

            feat = QgsGeometry().fromPoint( QgsPoint(x, y) )

            nearest = self._gridIndex.nearestNeighbor(QgsPoint(x, y), 4)
            for n in nearest:
                f = self.gridLayer.getFeatures(request=QgsFeatureRequest(n))
                for g in f:
                    values.append( g.attribute("HEIGHT") )
                    distances.append( g.geometry().distance(feat) )

            return self._inverseDistanceWeighted(values, distances, power)


    def _getIntersectionElevation(self, x, y):

        nearest = self._gridIndex.nearestNeighbor(QgsPoint(x, y), 1)
        f = self.gridLayer.getFeatures(request=QgsFeatureRequest(nearest[0]))
        for g in f:
            intersectElevation = g.attribute("HEIGHT")

        return intersectElevation


    def _isAtIntersection(self, x, y):

        if x % self.gridInterval == 0 and y % self.gridInterval == 0:
            return True
        else:
            return False


    def _inverseDistanceWeighted(self, values, distances, power):

        top = 0
        bottom = 0
        for value, distance in zip(values, distances):
            top += value/(distance**power)
            bottom +=  1/(distance**power)

        return top/bottom

