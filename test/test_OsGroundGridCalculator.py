# -*- coding: utf-8 -*-

import os, sys
import unittest
from qgis.core import (
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer)

from GBElevation.models import *

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()

#Loading NTF Files
path = os.path.join(os.path.dirname(__file__), 'testdata', 'NT48SE.NTF')
title = 'NT48SE_TestOsGroundGridCalculator'
layer = QgsVectorLayer(path, title, 'ogr')
NT48SE = OsGroundGridCalculator(layer, 10)
NT48 = OsGroundGridCalculator(layer, 50)

class TestOsGroundGridCalculator(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""


    def test_calculateElevationAtGridIntersection(self):
        """Test Elevation for 10m at intersections"""

        self.assertEqual( NT48SE.calculateElevation(346790, 683350), -2)
        self.assertEqual( NT48SE.calculateElevation(346790, 683360), -2)
        self.assertEqual( NT48SE.calculateElevation(346800, 682740), 36.09999847412109375)
        self.assertEqual( NT48SE.calculateElevation(346800, 682750), 35.90000152587890625)
        self.assertEqual( NT48SE.calculateElevation(346800, 682760), 35.5)
        self.assertEqual( NT48SE.calculateElevation(346790, 683080), 16.10000038146972656)
        self.assertEqual( NT48SE.calculateElevation(346790, 683090), 9)
        self.assertEqual( NT48SE.calculateElevation(346790, 683040), 22.10000038146972656)
        self.assertEqual( NT48SE.calculateElevation(346790, 683050), 21)
        self.assertEqual( NT48SE.calculateElevation(346790, 683060), 19.79999923706054688)
        self.assertEqual( NT48SE.calculateElevation(346790, 683070), 18.20000076293945312)


    def test_isAtIntersection(self):
        """Test is At Intersection"""
 
        self.assertTrue( NT48SE._isAtIntersection(346790,683330))
        self.assertTrue( NT48SE._isAtIntersection(346800,682750))
        self.assertTrue( NT48._isAtIntersection(346800,682750)) #TEST 50M

        self.assertFalse( NT48._isAtIntersection(346800,682740))
        self.assertFalse( NT48._isAtIntersection(346826,682745.2))

    def test_getNodeFeatureIds(self):
        """Test providing an x an y and receiving the IDs of surrounding points"""

        returned_nodes = [1,2, 502, 503]
        self.assertEqual( NT48SE._getClosestNodeFeatureIds(305004.6, 705004.8), returned_nodes )
        
    def test_getIntersectionNode(self):
        """Test providing an x an y and receive the ID of the intersection points"""

        returned_nodes = [90015]
        self.assertEqual( NT48SE._getIntersectionNode(346790, 683350), returned_nodes )
        


if __name__ == '__main__':
    unittest.main()
