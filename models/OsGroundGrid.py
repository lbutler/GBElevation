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

import os
from qgis.core import QgsVectorLayer, QgsPoint, QgsGeometry, QgsFeatureRequest, QgsMapLayerRegistry

from GBElevation.models import *


class OsGroundGrid:

    def __init__(self, updateLayer, featureIds, gridName, gridPath, elevationAttribute, interpolation, gridSpacing):
        self.updateLayer = updateLayer
        
        self.gridName = gridName
        self.elevationAttribute = elevationAttribute
        self.interpolation = interpolation
        self.gridSpacing = gridSpacing

        request = QgsFeatureRequest()
        request.setFilterFids(featureIds)
        self.features = updateLayer.getFeatures(request)

        self.layer = QgsVectorLayer(gridPath, gridName, 'ogr')

        if self.interpolation == 0:
            self.grid = OSGroundGridCalculatorBilinear(self.layer, self.gridSpacing)
        else:
            self.grid = OSGroundGridCalculatorIDW(self.layer, self.gridSpacing,2)

    def run(self):

        dp = self.updateLayer.dataProvider()

        #request = QgsFeatureRequest()
        #request.setSubsetOfAttributes([])
        #request.setFlags(QgsFeatureRequest.NoGeometry)

        updateMap = {}
        updateFieldIdx = dp.fields().indexFromName(self.elevationAttribute)

        for feature in self.features:
            elevation = self.grid.calculateElevation( feature.geometry(), self.updateLayer.crs() )
            updateMap[feature.id()] = { updateFieldIdx: elevation}

        dp.changeAttributeValues( updateMap )

        QgsMapLayerRegistry.instance().removeMapLayer( self.layer.id() )


