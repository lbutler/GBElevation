# -*- coding: utf-8 -*-

import os, sys
import unittest
from qgis.core import QgsVectorLayer, QgsField, QgsPoint, QgsFeature, QgsGeometry
from PyQt4.QtCore import QVariant

from GBElevation.models import *

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()



class TestOsLandform(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        
        directory = os.path.join(os.path.dirname(__file__), 'testdata' )
        interpolation = 0

        # create layer
        self.vl = QgsVectorLayer("Point?crs=epsg:27700&field=id:integer&field=height:double(20,8)&index=yes", "temporary_points", "memory")
        pr = self.vl.dataProvider()

        testQgsPoints = [QgsPoint(246800, 682740), QgsPoint(346800, 682740), QgsPoint(346800, 682740)]
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
        self.vl.updateExtents()



        self.osLandformObject = OsLandform(self.vl, 'height', directory, 0, 10)

#    def test__createGridDictionary(self):
#        """Tests createGridDictionary"""
#
#        self.osLandformObject._createGridDictionary()
#        
#        self.assertEqual( True, False)
#
#
#    def test__createGrids(self):
#        """Tests _createGrids"""
#
#        self.osLandformObject._createGridDictionary()
#        self.osLandformObject._createGrids()
#        
#        self.assertEqual( True, False)

    def test__run(self):
        """Tests _run"""

        self.osLandformObject.run()
        features = self.vl.getFeatures()
        for f in features:
            print f["height"]

        self.assertEqual( True, False) 










