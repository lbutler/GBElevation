# -*- coding: utf-8 -*-

import os, sys
import unittest
from qgis.core import QgsVectorLayer, QgsField, QgsPoint, QgsFeature, QgsGeometry
from PyQt4.QtCore import QVariant

from GBElevation.models import *

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()



class TestOsGroundGrid(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        
        directory = os.path.join(os.path.dirname(__file__), 'testdata' )
        gridName = 'NT48SE'

        # create layer
        self.vl = QgsVectorLayer("Point?crs=epsg:27700&field=id:integer&field=height:double(20,8)&index=yes", "temporary_points", "memory")
        pr = self.vl.dataProvider()
        
        # add a feature
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(346800, 682740)))
        fet.setAttributes([2, None])
        pr.addFeatures([fet])
        
        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        self.vl.updateExtents()
        self.nt48se = OsGroundGrid(self.vl, self.vl.getFeatures(), gridName, directory)


    def test_run(self):
        """Tests run"""
        
        self.nt48se.run()

        features = self.vl.getFeatures()
        for f in features:
          self.assertEqual( f["height"], 36.09999847412109375 ) 













