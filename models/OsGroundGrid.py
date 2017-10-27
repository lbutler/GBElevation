# -*- coding: utf-8 -*-

import os
from qgis.core import QgsVectorLayer, QgsPoint, QgsGeometry, QgsFeatureRequest, QgsMapLayerRegistry

from GBElevation.models import *


class OsGroundGrid:

	def __init__(self, updateLayer, features, gridName, directory):
		self.updateLayer = updateLayer
		self.features = features
		self.gridName = gridName

		path = os.path.join(directory, gridName + '.NTF')
		self.layer = QgsVectorLayer(path, gridName, 'ogr')

		self.grid = OsGroundGridCalculator(self.layer, 10, 2)

	def run(self):

		dp = self.updateLayer.dataProvider()

		request = QgsFeatureRequest()
		request.setSubsetOfAttributes([])
		request.setFlags(QgsFeatureRequest.NoGeometry)

		updateMap = {}
		updateFieldIdx = dp.fields().indexFromName('height')

		for feature in self.features:
			elevation = self.grid.calculateElevation( feature.geometry().asPoint().x(), feature.geometry().asPoint().y() )
			updateMap[feature.id()] = { updateFieldIdx: elevation}

		dp.changeAttributeValues( updateMap )

		QgsMapLayerRegistry.instance().removeMapLayer( self.layer.id() )


