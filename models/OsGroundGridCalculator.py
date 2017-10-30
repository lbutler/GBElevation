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
            return self._useAlgorithm(x, y)


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
