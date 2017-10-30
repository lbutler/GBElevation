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


class TestOsGroundGridCalculatorIDW(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        #Loading NTF Files
        path = os.path.join(os.path.dirname(__file__), 'testdata', 'NT48SE.NTF')
        title = 'NT48SE'
        layer = QgsVectorLayer(path, title, 'ogr')
        self.NT48SE = OSGroundGridCalculatorIDW(layer, 10,2 )
        self.NT48 = OSGroundGridCalculatorIDW(layer, 50, 1)


    def test_calculateElevation10m(self):
        """Test Elevation for 10m"""

        self.assertAlmostEqual( self.NT48SE.calculateElevation(346895, 682505), 38.875)
        self.assertAlmostEqual( self.NT48SE.calculateElevation(346892.5, 682505), 38.81944444)


    def test_inverseDistanceWeighted(self):
        """Manual check of IDW function"""

        values = [20,10,30,35]
        distance = [9.60468635614927, 8.5, 6.5, 4.7169905660283]

        answer = 28.27963613

        self.assertAlmostEqual( self.NT48SE._inverseDistanceWeighted(values, distance), answer)

        values = [20,10,30,35]
        distance = [9.60468635614927, 8.5, 6.5, 4.7169905660283]

        answer = 26.02779539

        self.assertAlmostEqual( self.NT48._inverseDistanceWeighted(values, distance), answer)



if __name__ == '__main__':
    unittest.main()
