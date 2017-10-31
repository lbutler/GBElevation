# -*- coding: utf-8 -*-

import os
from qgis.core import QgsVectorLayer, QgsPoint, QgsGeometry, QgsFeatureRequest, QgsMapLayerRegistry

from GBElevation.models import *


class OsGroundGrid:

    def __init__(self, updateLayer, featureIds, gridName, directory, elevationAttribute):
        self.updateLayer = updateLayer
        
        self.gridName = gridName
        self.elevationAttribute = elevationAttribute

        request = QgsFeatureRequest()
        request.setFilterFids(featureIds)
        self.features = updateLayer.getFeatures(request)

        path = os.path.join(directory, gridName + '.NTF')
        self.layer = QgsVectorLayer(path, gridName, 'ogr')

        self.grid = OSGroundGridCalculatorIDW(self.layer, 10, 2)

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


