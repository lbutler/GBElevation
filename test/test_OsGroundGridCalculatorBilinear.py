# -*- coding: utf-8 -*-

import os, sys
import unittest
from qgis.core import (
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
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


class TestOsGroundGridCalculatorBilinear(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""

    def test_calculateElevation10mIWvalues(self):
        """TestOsGroundGridCalculatorBilinear"""

        self.assertAlmostEqual( NT48SE.calculateElevation(346811, 683070), 21.05)
        self.assertAlmostEqual( NT48SE.calculateElevation(346837, 682822), 34.43, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation(346824, 682866), 30.608, 3)


        self.assertAlmostEqual( NT48SE.calculateElevation(346850, 682740), 38.3, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation(346825, 683335), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation(346823, 683334), -2, 3)


        self.assertAlmostEqual( NT48SE.calculateElevation(346830, 683180), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation(346830, 683170), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation(346820, 683180), -2, 3)
        self.assertAlmostEqual( NT48SE.calculateElevation(346820, 683170), -2, 3)
        
        self.assertAlmostEqual( NT48SE.calculateElevation(346826, 683174), -2, 3)



    def test_calculateElevation10mFails(self):
        """Failed Bilinear Interploation"""
        self.assertAlmostEqual( NT48SE.calculateElevation(346821, 683247), -1.993, 3)



    def test_bilinearInterpolation(self):
        """Manual check of Bilinear Interpolation function"""


        points = [QgsPoint(800, 60), QgsPoint(810, 60), QgsPoint(800, 50), QgsPoint(810, 50)]
        values = [20,10,30,35]
        answer = 22.8

        self.assertAlmostEqual( NT48SE._bilinearInterpolation(803, 56, values, points), answer)


        points = [QgsPoint(800, 60), QgsPoint(810, 60), QgsPoint(800, 50), QgsPoint(810, 50)]
        values = [-2,-2,-2,-2]
        answer = -2

        self.assertAlmostEqual( NT48SE._bilinearInterpolation(803, 56, values, points), answer)



if __name__ == '__main__':
    unittest.main()
