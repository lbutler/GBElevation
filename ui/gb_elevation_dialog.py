# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GBElevationDialog
                                 A QGIS plugin
 Calculate elevation of points from 10m & 50m OS NTF files
                             -------------------
        begin                : 2017-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luke Butler
        email                : lukepbutler@gmail.com
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog, QListWidgetItem, QBrush, QColor

from qgis.core import QgsMapLayerRegistry, QGis

from GBElevation.models import OsTileLocator, OsLandform

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gb_elevation_dialog_base.ui'))


class GBElevationDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(GBElevationDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface


        # Link Actons
        self.dtmFolderButton.clicked.connect(self.selectDtmFolderLocation)
        self.pointLayersComboBox.currentIndexChanged.connect(self._pointsLayerChanged)


    def run(self):

        layerId =  self.pointLayersComboBox.itemData( self.pointLayersComboBox.currentIndex() )
        registry = QgsMapLayerRegistry.instance()
        layer = registry.mapLayer( layerId )

        elevationAttribute = self.attributeComboBox.itemText(self.attributeComboBox.currentIndex())
        dtmDirectory = self.dtmFolder.text()
        interpolation = self.interpolationMethodComboBox.currentIndex()
        gridSpacing = 10

        self.osLandformObject = OsLandform(layer, elevationAttribute, dtmDirectory, interpolation, gridSpacing)
        self.osLandformObject.run()


    def prepareForm(self):
        self.addPointLayers()

    def selectDtmFolderLocation(self):
        folderPath = ''
        filename = QFileDialog.getExistingDirectory(self, "Open Directory", folderPath, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks);
        self.dtmFolder.setText(filename)

    def addPointLayers(self):
        self.pointLayersComboBox.clear()
        layers = self.iface.legendInterface().layers()
        for layer in layers:
            if layer.geometryType() == QGis.Point:
                self.pointLayersComboBox.addItem(layer.name(), layer.id())


    def _pointsLayerChanged(self, idx):

        layerId=  self.pointLayersComboBox.itemData(idx)
        registry = QgsMapLayerRegistry.instance()
        layer = registry.mapLayer( layerId )

        self._updateAttributes(layer)
        self._updateDtmListItems(layer)

        #self._getDtmsForLayer(layerId)


    def _updateAttributes(self, layer):

        prov = layer.dataProvider()

        field_names = []
        for field in prov.fields():
            if field.type() == 6: # Type is double
                field_names.append(field.name())

        self.attributeComboBox.clear()
        self.attributeComboBox.addItems(field_names)


    def _updateDtmListItems(self, layer):

        self.dtmList.clear()
        dtms = list(self._getDtmsForLayer(layer))

        redBrush = QBrush(QColor(255, 0, 0, 255))
        redBrush.setStyle(1)

        greenBrush = QBrush(QColor(0, 255, 0, 255))
        greenBrush.setStyle(1)

        for dtm in dtms:
            newListItem = QListWidgetItem()
            newListItem.setText(dtm)
            if self._dtmInFolder(dtm):
                newListItem.setBackground(greenBrush)
            else:
                newListItem.setBackground(redBrush)
            self.dtmList.insertItem(0, newListItem)


    def _getDtmsForLayer(self, layer):
        output = set()
        features = layer.getFeatures()
        for feature in features:
            featurePoint = feature.geometry().asPoint()
            output.add( OsTileLocator( featurePoint.x(), featurePoint.y() ).fiveKmSqTile() )

        return output


    def _dtmInFolder(self, dtmName):
        path = os.path.join(self.dtmFolder.text(), dtmName + '.NTF')
        return os.path.isfile(path)






        




