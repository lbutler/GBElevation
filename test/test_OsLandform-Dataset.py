# -*- coding: utf-8 -*-

import os, sys
import unittest
from qgis.core import QgsVectorLayer, QgsField, QgsPoint, QgsFeature, QgsGeometry
from PyQt4.QtCore import QVariant

from GBElevation.models import *

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()


directory = os.path.join(os.path.dirname(__file__), 'testdata', 'NO')
interpolation = 0
# create layer
vl = QgsVectorLayer("Point?crs=epsg:27700&field=id:integer&field=height:double(20,8)&index=yes", "temporary_points", "memory")
pr = vl.dataProvider()
testQgsPoints = [
QgsPoint(337797.84,754389.19),
QgsPoint(337847.85,754576.06),
QgsPoint(337868.18,754387.36),
QgsPoint(338040.12,753937.73),
QgsPoint(338049.32,753862.54),
QgsPoint(337804.72,754026.93),
QgsPoint(337807.15,753980.72),
QgsPoint(337824.33,754095.58),
QgsPoint(337792.50,754226.34),
QgsPoint(338041.33,754263.26),
QgsPoint(337927.06,753974.65),
QgsPoint(337925.07,754266.72),
QgsPoint(337954.32,754388.37),
QgsPoint(336924.98,756754.17),
QgsPoint(338701.77,757109.63),
QgsPoint(336270.51,757592.27),
QgsPoint(337058.01,755681.47),
QgsPoint(337642.98,755680.71),
QgsPoint(336635.15,759343.05),
QgsPoint(336755.31,755437.64),
QgsPoint(337650.25,758425.33),
QgsPoint(337644.52,758432.75),
QgsPoint(337621.27,758670.79),
QgsPoint(338401.04,757842.06),
QgsPoint(338078.86,760632.25),
QgsPoint(338369.56,760204.79),
QgsPoint(338655.41,760230.23),
QgsPoint(338700.19,760138.58),
QgsPoint(338563.19,759340.32),
QgsPoint(339096.42,759600.07),
QgsPoint(339380.84,759687.25),
QgsPoint(339515.90,759728.95),
QgsPoint(349408.47,779616.53),
QgsPoint(349262.68,779694.81),
QgsPoint(349154.94,779732.25),
QgsPoint(349060.60,779848.36),
QgsPoint(350829.11,778925.96),
QgsPoint(337986.24,754320.95),
QgsPoint(338746.97,759683.08),
QgsPoint(338743.01,759686.33),
QgsPoint(338243.87,760621.14),
QgsPoint(338634.62,760254.52),
QgsPoint(338715.84,760076.11),
QgsPoint(337619.89,758657.6),
QgsPoint(337824.00,760075),
QgsPoint(337983.78,754734.45),
QgsPoint(338024.10,754693.72),
QgsPoint(337967.66,754640.23),
QgsPoint(337768.22,754116.27),
QgsPoint(337952.32,753891.45),
QgsPoint(338068.51,760636.02),
QgsPoint(337893.15,754594.94),
QgsPoint(337945.03,754588.21)
]
features = []
for testPoint in testQgsPoints:    
    # add a feature
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPoint(testPoint))
    fet.setAttributes([2, None])
    features.append(fet)

pr.addFeatures(features)
        
# update layer's extent when new features have been added
# because change of extent in provider is not propagated to the layer
vl.updateExtents()
osLandformObject = OsLandform(vl, 'height', directory, 0, 10)


class TestOsLandform(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        pass


    def test__run(self):
        """Tests _run"""

        testResults = [143.13,
        148.49,
        147.33,
        138.2,
        136.47,
        146.59,
        145.33,
        144.84,
        146.88,
        142.96,
        141.13,
        142.27,
        149.1,
        214.4,
        138.8,
        198.11,
        164.71,
        162.34,
        185.37,
        157.45,
        138.8,
        138.8,
        174.16,
        161.6,
        230.17,
        217.77,
        196.16,
        196.09,
        163.48,
        156.21,
        135.38,
        129.1,
        200.56,
        199.75,
        197.85,
        201,
        194.66,
        144.78,
        163.7,
        164.08,
        228.07,
        195.1,
        189.9,
        172.14,
        237.49,
        154.31,
        154.7,
        152.51,
        149.03,
        139.36,
        230.62,
        150.72,
        151.8]

        height_test = []

        osLandformObject.run()
        features = vl.getFeatures()
        for f in features:
            height_test.append(f["height"])

        for idx, height in enumerate(height_test):
            self.assertAlmostEqual( height, testResults[idx], 2) 

        










