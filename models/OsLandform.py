# -*- coding: utf-8 -*-

import os
from collections import defaultdict

from PyQt4 import QtCore
from qgis.core import QgsVectorLayer

from GBElevation.models import *


class OsLandform(QtCore.QObject):

    def __init__(self, layer, elevationAttribute, dtmDirectory, interpolation, gridSpacing, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        
        self.layer = layer
        self.elevationAttribute = elevationAttribute
        self.dtmDirectory = dtmDirectory
        self.interpolation = interpolation
        self.gridSpacing = gridSpacing
        self._gridDictionary = defaultdict(list)
        self._grids = []

        self.processed = 0
        self.percentage = 0
        self.abort = False
    
    def run(self):
        try:
            self._createGridDictionary()
            self.feature_count = len(self._gridDictionary)

            for gridRef in self._gridDictionary:
                if self.abort is True:
                    self.killed.emit()
                    break
                if self._dtmExists(gridRef):
                    grid = OsGroundGrid(self.layer, self._gridDictionary[gridRef], gridRef, self.dtmDirectory, self.elevationAttribute, self.interpolation, self.gridSpacing)
                    grid.run()
                    self.calculate_progress()

        except:
            import traceback
            self.error.emit(traceback.format_exc())
            self.finished.emit(False)
        else:
            self.finished.emit(True)

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


    def calculate_progress(self):
        self.processed = self.processed + 1
        percentage_new = (self.processed * 100) / self.feature_count
        if percentage_new > self.percentage:
            self.percentage = percentage_new
            self.progress.emit(self.percentage)

    def kill(self):
        self.abort = True

    progress = QtCore.pyqtSignal(int)
    error = QtCore.pyqtSignal(str)
    killed = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal(bool)
