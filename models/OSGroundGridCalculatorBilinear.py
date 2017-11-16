# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry, QgsRectangle

from GBElevation.models import *

class OSGroundGridCalculatorBilinear(OsGroundGridCalculator):

    def __init__(self, gridLayer, gridInterval):

        OsGroundGridCalculator.__init__(self, gridLayer, gridInterval)

    def _useAlgorithm(self, x, y):

        values = []
        points = []

        pointTopLeft = QgsPoint(x - self.gridInterval, y + self.gridInterval)
        pointBottomRight  = QgsPoint(x + self.gridInterval, y - self.gridInterval)
        square = QgsRectangle(pointTopLeft, pointBottomRight)

        nearest = self._gridIndex.intersects(square)
        for nearid in nearest:
            f = self.allfeatures[nearid]
            values.append( f.attribute("HEIGHT") )
            points.append( f.geometry().asPoint() )

        return self._bilinearInterpolation(x, y, values, points)

    def _bilinearInterpolation(self, x, y, values, points):

        result = 0

        for value, point in zip(values, points):

            width = self.gridInterval - abs(point.x() - x)
            height = self.gridInterval - abs(point.y() - y)

            area = (width * height ) / self.gridInterval ** 2
            result += area *value

        return result
