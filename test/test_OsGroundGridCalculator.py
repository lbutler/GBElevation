# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GBElevation
                                 A QGIS plugin
 Calculate elevation of points from 10m & 50m OS NTF files
                              -------------------
        begin                : 2017-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luke Butler - Matrado Limited
        email                : luke@matrado.ca
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os, sys
import unittest
from qgis.core import (
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsGeometry,
    QgsPoint)

from GBElevation.models import *

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()

#Loading NTF Files
path = os.path.join(os.path.dirname(__file__), 'testdata', 'NT48SE.NTF')
title = 'NT48SE_TestOsGroundGridCalculator'
layer = QgsVectorLayer(path, title, 'ogr')
NT48SE = OsGroundGridCalculator(layer, 10)

path_NT48 = os.path.join(os.path.dirname(__file__), 'testdata', 'nt48.ntf')
layer_NT48 = QgsVectorLayer(path_NT48, '50m Grid NT48', 'ogr')
NT48 = OsGroundGridCalculator(layer_NT48, 50)

crs27700 = QgsCoordinateReferenceSystem(27700) 

class TestOsGroundGridCalculator(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""


    def test_calculateElevationAtGridIntersection(self):
        """Test Elevation for 10m at intersections"""

        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683350), crs27700) , -2)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683360), crs27700) , -2)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346800, 682740), crs27700) , 36.09999847412109375)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346800, 682750), crs27700) , 35.90000152587890625)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346800, 682760), crs27700) , 35.5)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683080), crs27700) , 16.10000038146972656)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683090), crs27700) , 9)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683040), crs27700) , 22.10000038146972656)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683050), crs27700) , 21)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683060), crs27700) , 19.79999923706054688)
        self.assertEqual( NT48SE.calculateElevation( self.geometryFromPoint(346790, 683070), crs27700) , 18.20000076293945312)


    def test_isAtIntersection(self):
        """Test is At Intersection"""
 
        self.assertTrue( NT48SE._isAtIntersection(346790,683330))
        self.assertTrue( NT48SE._isAtIntersection(346800,682750))
        self.assertTrue( NT48._isAtIntersection(346800,682750)) #TEST 50M

        self.assertFalse( NT48._isAtIntersection(346800,682740))
        self.assertFalse( NT48._isAtIntersection(346826,682745.2))

    def test_getNodeFeatureIds(self):
        """Test providing an x an y and receiving the IDs of surrounding points"""
        #10m test
        self.assertEqual( NT48SE._getClosestNodeFeatureIds(345003.02,680001.95), [1,2, 502, 503] )
        self.assertEqual( NT48SE._getClosestNodeFeatureIds(347554.33,682572.43), [128013, 128014, 128514, 128515] )
        self.assertEqual( NT48SE._getClosestNodeFeatureIds(349943.97,684963.43), [247991, 247992, 248492, 248493] )

        #50m test
        self.assertEqual( NT48._getClosestNodeFeatureIds(340021.3,680015.1), [1,2, 402, 403] )
        self.assertEqual( NT48._getClosestNodeFeatureIds(340167.5,680113.8), [1206, 1207, 1607, 1608] )
        self.assertEqual( NT48._getClosestNodeFeatureIds(357022.2,699213.6), [136725, 136726, 137126, 137127] )

        
    def test_getIntersectionNode(self):
        """Test providing an x an y and receive the ID of the intersection points"""

        returned_nodes = [90015]
        self.assertEqual( NT48SE._getIntersectionNode(346790, 683350), returned_nodes )




    def geometryFromPoint(self, x, y):
        return QgsGeometry.fromPoint( QgsPoint(x, y) )

if __name__ == '__main__':
    unittest.main()
