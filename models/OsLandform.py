# -*- coding: utf-8 -*-

import os
from collections import defaultdict

from qgis.core import QgsVectorLayer

from GBElevation.models import *

import time

class OsLandform:

    def __init__(self, layer, elevationAttribute, dtmDirectory, interpolation, gridSpacing):
        
        self.layer = layer
        self.elevationAttribute = elevationAttribute
        self.dtmDirectory = dtmDirectory
        self.interpolation = interpolation
        self.gridSpacing = gridSpacing
        self._gridDictionary = defaultdict(list)
        self._grids = []


    def run(self):

        time1 =  time.time()

        self._createGridDictionary()

        for gridRef in self._gridDictionary:
            if self._dtmExists(gridRef):
                grid = OsGroundGrid(self.layer, self._gridDictionary[gridRef], gridRef, self.dtmDirectory, self.elevationAttribute, self.interpolation, self.gridSpacing)
                grid.run()


        print "Time to run: " + str(time1 - time.time())

    def _createGrids(self):

        for gridRef in self._gridDictionary:
            if self._dtmExists(gridRef):
                self._grids.append( OsGroundGrid(self.layer, self._gridDictionary[gridRef], gridRef, self.dtmDirectory, self.elevationAttribute, self.interpolation, self.gridSpacing) )


    def _createGridDictionary(self):

        for feature in self.layer.getFeatures():
            featurePoint = feature.geometry().asPoint()
            if self.gridSpacing == 10:
                self._gridDictionary[ OsTileLocator( featurePoint.x(), featurePoint.y() ).fiveKmSqTile() ].append(feature.id())
            else:
                self._gridDictionary[ OsTileLocator( featurePoint.x(), featurePoint.y() ).tenKmSqTile() ].append(feature.id())


    def _dtmExists(self, dtmName):
        path = os.path.join(self.dtmDirectory, dtmName + '.NTF')
        return os.path.isfile(path)
