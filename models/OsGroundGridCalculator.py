# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsPoint, QgsFeatureRequest,QgsGeometry

class OsGroundGridCalculator:

    def __init__(self, gridLayer, gridInterval):

        self.gridLayer = gridLayer
        self.gridInterval = gridInterval
        self.featuresHeights = self.gridLayer.getDoubleValues("Height")
 
    def calculateElevation(self, x, y):

        if self._isAtIntersection(x, y):
            return self._getIntersectionElevation(x,y)
        else:
            return self._useAlgorithm(x, y)


    def _getIntersectionElevation(self, x, y):

        featureId = self._getIntersectionNode(x,y)[0]
        return self.featuresHeights[0][featureId - 1]


    def _isAtIntersection(self, x, y):

        if x % self.gridInterval == 0 and y % self.gridInterval == 0:
            return True
        else:
            return False


    
    def _getClosestNodeFeatureIds(self, x, y):
        """ NTF are always loaded with the first feature in the bottom left hand corner being 1L
            and then counting up by one in the Y direction for 501 nodes, it then loops to the bottom
            second column which is 502L
            We are using this function to figure out the IDs of the four closest nodes to any XY pair
            so we can quickly grab them without a spatial index, crazy risky stuff  """
        if self.gridInterval == 10:
            rowsInDtm = 501
            modulas = 5000
        else:
            rowsInDtm = 401
            modulas = 20000


        xDirection = 1 + int((x % modulas)/self.gridInterval) * rowsInDtm
        yDirection = int((y % modulas)/self.gridInterval)

        firstNode = xDirection + yDirection

        return [ firstNode,  firstNode + 1,  firstNode + rowsInDtm ,  firstNode + rowsInDtm + 1    ]

    def _getIntersectionNode(self, x, y):
        xDirection = 1 + (int((x % 5000)/10) * 501)
        yDirection = int((y % 5000)/10)
        return [xDirection + yDirection]

