# -*- coding: utf-8 -*-
"""
 GBElevation - QGIS Plugin
 *************************
 Copyright (c) 2017 Luke Butler (luke@matrado.ca) - Matrado Limited
 Licence - github.com/lbutler/GBElevation/blob/master/LICENSE
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
            elevation = self.grid.calculateElevation( feature.geometry().asPoint().x(), feature.geometry().asPoint().y() )
            updateMap[feature.id()] = { updateFieldIdx: elevation}

        dp.changeAttributeValues( updateMap )

        QgsMapLayerRegistry.instance().removeMapLayer( self.layer.id() )


