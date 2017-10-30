# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry

from GBElevation.models import *

class OSGroundGridCalculatorBilinear(OsGroundGridCalculator):

    def __init__(self, gridLayer, gridInterval):

        OsGroundGridCalculator.__init__(self, gridLayer, gridInterval)

    def _useAlgorithm(self, x, y):

        values = []
        points = []

        feat = QgsGeometry().fromPoint( QgsPoint(x, y) )

        nearest = self._gridIndex.nearestNeighbor(QgsPoint(x, y), 4)
        for n in nearest:
            f = self.gridLayer.getFeatures(request=QgsFeatureRequest(n))
            for g in f:
                values.append( g.attribute("HEIGHT") )
                points.append( g.geometry().asPoint() )

        return self._bilinearInterpolation(x, y, values, points)

    def _bilinearInterpolation(self, x, y, values, points):

        result = 0 

        for value, point in zip(values, points):

            width = self.gridInterval - abs(point.x() - x)
            height = self.gridInterval - abs(point.y() - y)

            area = (width * height ) / self.gridInterval ** 2
            result += area *value

        return result
