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
title = 'NT48SE_TestOsGroundGridCalculatorIDW'
layer = QgsVectorLayer(path, title, 'ogr')
NT48SE = OSGroundGridCalculatorBilinear(layer, 10 )
NT48 = OSGroundGridCalculatorBilinear(layer, 50)

crs27700 = QgsCoordinateReferenceSystem(27700) 
class TestOsGroundGridCalculatorBilinear(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""

    def test_calculateElevation10mIWvalues(self):
        """TestOsGroundGridCalculatorBilinear"""

        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346811, 683070), crs27700), 21.05)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346837, 682822), crs27700), 34.43, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346824, 682866), crs27700), 30.608, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346850, 682740), crs27700), 38.3, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346825, 683335), crs27700), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346823, 683334), crs27700), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346830, 683180), crs27700), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346830, 683170), crs27700), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346820, 683180), crs27700), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346820, 683170), crs27700), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346826, 683174), crs27700), -2, 3)



    def test_calculateElevation10mFails(self):
        """Failed Bilinear Interploation"""
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(346821, 683247), crs27700), -1.993, 3)



    def test_bilinearInterpolation(self):
        """Manual check of Bilinear Interpolation function"""

        answer = 22.8

        nodes = { 1: {"geometry": QgsPoint(800, 60), "height": 20},
            2: {"geometry": QgsPoint(810, 60), "height": 10},
            3: {"geometry": QgsPoint(800, 50), "height": 30},
            4: {"geometry": QgsPoint(810, 50), "height": 35} 
            }

        self.assertAlmostEqual( NT48SE._bilinearInterpolation(803, 56, nodes), answer)


        answer = -2

        nodes = { 1: {"geometry": QgsPoint(800, 60), "height": -2},
            2: {"geometry": QgsPoint(810, 60), "height": -2},
            3: {"geometry": QgsPoint(800, 50), "height": -2},
            4: {"geometry": QgsPoint(810, 50), "height": -2} 
            }

        self.assertAlmostEqual( NT48SE._bilinearInterpolation(803, 56, nodes), answer)


    def test__otherProjections(self):
        """ Testing using alternative projections """
        crs4326 = QgsCoordinateReferenceSystem(4326)

        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(-2.8549735972 , 56.0357146783), crs4326), 30.608, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(-2.85453137032 , 56.0345856327), crs4326), 38.3, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(-2.85505073723 , 56.0399281074), crs4326), -2, 3)

        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(-2.85533366926 , 56.0345800718), crs4326) , 36.09999847412109375, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation( self.geometryFromPoint(-2.85533565671 , 56.034669908), crs4326) , 35.90000152587890625, 3)



    def geometryFromPoint(self, x, y):
        return QgsGeometry.fromPoint( QgsPoint(x, y) )


if __name__ == '__main__':
    unittest.main()
