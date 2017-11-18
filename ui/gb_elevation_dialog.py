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

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import QFileDialog, QListWidgetItem, QBrush, QColor, QInputDialog, QLineEdit, QProgressBar
from PyQt4.QtCore import QVariant, Qt

from qgis.core import QgsMapLayerRegistry, QGis, QgsVectorDataProvider, QgsField, QgsMapLayer
from qgis.gui import QgsMessageBar

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
        self.dtmFolder.editingFinished.connect(self._updateDtmListItems)
        self.pointLayersComboBox.currentIndexChanged.connect(self._pointsLayerChanged)
        self.attributeButton.clicked.connect(self._createElevationAttribute)

        self.os10mRadioButton.toggled.connect(self._updateDtmListItems)
        self.os50mRadioButton.toggled.connect(self._updateDtmListItems)

    def run(self):
        layer = self._getCurrentSelectedLayer()
        elevationAttribute = self.attributeComboBox.itemText(self.attributeComboBox.currentIndex())
        dtmDirectory = self.dtmFolder.text()
        interpolation = self.interpolationMethodComboBox.currentIndex()
        gridSpacing = self._getGridSpacing()

        self._progressbar_create()


        thread = self.thread = QtCore.QThread()
        worker = self.worker = OsLandform(layer, elevationAttribute, dtmDirectory, interpolation, gridSpacing)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self._progressbar_update)
        worker.finished.connect(self._progressbar_clear)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(thread.quit)
        thread.start()

    def _progressbar_create(self):
        self.progressMessageBar = self.iface.messageBar().createMessage("Adding elevations to layer...")
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.progressMessageBar.layout().addWidget(self.progress)
        self.iface.messageBar().pushWidget(self.progressMessageBar, self.iface.messageBar().INFO)

    def _progressbar_clear(self):
        self.iface.messageBar().clearWidgets()
        if self.worker.abort:
            self.iface.messageBar().pushMessage("GB NTF Elevations", "Adding elevations was cancelled, not all elevations may have been set", level=QgsMessageBar.WARNING)
        else:
            self.iface.messageBar().pushMessage("GB NTF Elevations", "Elevations have been added", level=QgsMessageBar.INFO)

    def _progressbar_update( self, percent):
        # If they close the progressbar we assume they want to stop
        # I'm not sure of a better way to capture this so using an exception
        try:
            self.progress.setValue(percent)
        except RuntimeError:
            self.worker.abort = True


    def prepareForm(self):
        self.addPointLayers()

    def selectDtmFolderLocation(self):
        folderPath = ''
        filename = QFileDialog.getExistingDirectory(self, "Open Directory", folderPath, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks);
        self.dtmFolder.setText(filename)
        self._updateDtmListItems()

    def addPointLayers(self):
        self.pointLayersComboBox.clear()
        layers = self.iface.legendInterface().layers()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                self.pointLayersComboBox.addItem(layer.name(), layer.id())


    def _pointsLayerChanged(self, idx):

        if idx <> -1:
            layer = self._getCurrentSelectedLayer()

            self._updateAttributes(layer)
            self._updateDtmListItems()

        #self._getDtmsForLayer(layerId)


    def _updateAttributes(self, layer):

        prov = layer.dataProvider()

        field_names = []
        for field in prov.fields():
            if field.type() == 6: # Type is double
                field_names.append(field.name())

        self.attributeComboBox.clear()
        self.attributeComboBox.addItems(field_names)


    def _updateDtmListItems(self):

        layer = self._getCurrentSelectedLayer()
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
        gridSpacing = self._getGridSpacing()

        for feature in features:
            featurePoint = feature.geometry().asPoint()
            if gridSpacing == 10:
                output.add( OsTileLocator( featurePoint.x(), featurePoint.y() ).fiveKmSqTile() )
            else:
                output.add( OsTileLocator( featurePoint.x(), featurePoint.y() ).tenKmSqTile() )

        return output


    def _dtmInFolder(self, dtmName):
        path = os.path.join(self.dtmFolder.text(), dtmName + '.NTF')
        return os.path.isfile(path)


    def _createElevationAttribute(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            success = self._createAttribute(text)

            layer = self._getCurrentSelectedLayer()
            self._updateAttributes(layer)


    def _createAttribute(self, text):
        layer = self._getCurrentSelectedLayer()
        provider = layer.dataProvider()
        caps = provider.capabilities()
        # Check if attribute is already there, return "-1" if not
        ind = provider.fieldNameIndex(text)
        try:
           if ind == -1:
               if caps & QgsVectorDataProvider.AddAttributes:
                   res = provider.addAttributes( [ QgsField(text,QVariant.Double) ] )
                   layer.updateFields()
                   return True
               else:
                   self.iface.messageBar().pushMessage("Error", "Unable to update the selected layer, it may be read-only", level=QgsMessageBar.CRITICAL)
           else:
               self.iface.messageBar().pushMessage("Error", "The field '" + text + "' already exists in the selected layer", level=QgsMessageBar.CRITICAL)
        except:
            return False
            self.iface.messageBar().pushMessage("Error", "Unable to update the selected layer, it may be read-only", level=QgsMessageBar.CRITICAL)


    def _getCurrentSelectedLayer(self):
        layerId =  self.pointLayersComboBox.itemData( self.pointLayersComboBox.currentIndex() )
        registry = QgsMapLayerRegistry.instance()
        layer = registry.mapLayer( layerId )

        return layer

    def _getGridSpacing(self):
        if self.os10mRadioButton.isChecked():
            return 10
        else:
            return 50





