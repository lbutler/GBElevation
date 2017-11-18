# -*- coding: utf-8 -*-

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
