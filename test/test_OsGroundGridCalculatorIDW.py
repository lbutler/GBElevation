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
    QgsVectorLayer)

from GBElevation.models import *

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()

#Loading NTF Files
path = os.path.join(os.path.dirname(__file__), 'testdata', 'NT48SE-2.NTF')
title = 'NT48SE_TestOsGroundGridCalculatorIDW'
layer = QgsVectorLayer(path, title, 'ogr')
NT48SE = OSGroundGridCalculatorIDW(layer, 10,2 )
NT48 = OSGroundGridCalculatorIDW(layer, 50, 1)


class TestOsGroundGridCalculatorIDW(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""


    def test_calculateElevation10m(self):
        """Test Elevation for 10m"""

        self.assertAlmostEqual( NT48SE.calculateElevation(346895, 682505), 38.875)
        self.assertAlmostEqual( NT48SE.calculateElevation(346892.5, 682505), 38.81944444)


    def test_inverseDistanceWeighted(self):
        """Manual check of IDW function"""

        nodes = { 1: {"distance": 9.60468635614927, "height": 20},
            2: {"distance":  8.5, "height": 10},
            3: {"distance": 6.5, "height": 30},
            4: {"distance": 4.7169905660283, "height": 35} 
            }

        answer = 28.27963613

        self.assertAlmostEqual( NT48SE._inverseDistanceWeighted(nodes), answer)

        nodes = { 1: {"distance": 9.60468635614927, "height": 20},
            2: {"distance":  8.5, "height": 10},
            3: {"distance": 6.5, "height": 30},
            4: {"distance": 4.7169905660283, "height": 35} 
            }

        answer = 26.02779539

        self.assertAlmostEqual( NT48._inverseDistanceWeighted(nodes), answer)



if __name__ == '__main__':
    unittest.main()
