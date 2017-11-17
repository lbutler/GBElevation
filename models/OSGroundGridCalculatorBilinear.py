# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry, QgsRectangle

from GBElevation.models import *

class OSGroundGridCalculatorBilinear(OsGroundGridCalculator):

    def __init__(self, gridLayer, gridInterval):

        OsGroundGridCalculator.__init__(self, gridLayer, gridInterval)

    def _useAlgorithm(self, x, y):

        values = []
        points = []

        request = QgsFeatureRequest()
        request.setFilterFids(self._getClosestNodeFeatureIds(x,y))

        nearestFourGridNodes = self.gridLayer.getFeatures( request )
        for gridNode in nearestFourGridNodes:
            values.append( gridNode.attribute("HEIGHT") )
            points.append( gridNode.geometry().asPoint() )

        return self._bilinearInterpolation(x, y, values, points)

    def _bilinearInterpolation(self, x, y, values, points):

        result = 0

        for value, point in zip(values, points):

            width = self.gridInterval - abs(point.x() - x)
            height = self.gridInterval - abs(point.y() - y)

            area = (width * height ) / self.gridInterval ** 2
            result += area *value

        return result
