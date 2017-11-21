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

from GBElevation.models import *
from qgis.core import QgsGeometry, QgsPoint, QgsCoordinateReferenceSystem

import unittest

crs27700 = QgsCoordinateReferenceSystem(27700) 

class TestOsTileLocator(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        pass

    def test_hundredKmSqTile(self):
        """Test Hundred Km Sq Tile"""

        self.assertEqual( OsTileLocator( self.geometryFromPoint(541330,120443), crs27700 ).hundredKmSqTile(), 'TQ') 
        self.assertEqual( OsTileLocator( self.geometryFromPoint(593091,587066), crs27700 ).hundredKmSqTile() , 'OV')
        self.assertEqual( OsTileLocator( self.geometryFromPoint(358161,361649), crs27700 ).hundredKmSqTile(), 'SJ') 
        self.assertEqual( OsTileLocator( self.geometryFromPoint(337914,667001), crs27700 ).hundredKmSqTile(), 'NT') 

    def test_tenKmSqTile(self):
        """Test Ten Km Sq Tile"""

        self.assertEqual( OsTileLocator( self.geometryFromPoint(593091,587066), crs27700 ).tenKmSqTile(), 'OV98' )

    def test_tenKmqlTileForNtfGrid(self):
        """Test Ten Km Sq Tile for Ntf grid file"""
        self.assertEqual( OsTileLocator( self.geometryFromPoint(205609, 807137), crs27700 ).tenKmqlTileForNtfGrid(), 'NH00' ) #NH00
        self.assertEqual( OsTileLocator( self.geometryFromPoint(214717, 807395), crs27700 ).tenKmqlTileForNtfGrid(), 'NH00' ) #NH10
        self.assertEqual( OsTileLocator( self.geometryFromPoint(205265, 814784), crs27700 ).tenKmqlTileForNtfGrid(), 'NH00' ) #NH01
        self.assertEqual( OsTileLocator( self.geometryFromPoint(214631, 814870), crs27700 ).tenKmqlTileForNtfGrid(), 'NH00' ) #NH11
        self.assertEqual( OsTileLocator( self.geometryFromPoint(204664, 825181), crs27700 ).tenKmqlTileForNtfGrid(), 'NH02' ) #NH02
        self.assertEqual( OsTileLocator( self.geometryFromPoint(215147, 824752), crs27700 ).tenKmqlTileForNtfGrid(), 'NH02' ) #NH12
        self.assertEqual( OsTileLocator( self.geometryFromPoint(224684, 824838), crs27700 ).tenKmqlTileForNtfGrid(), 'NH22' ) #NH22
        self.assertEqual( OsTileLocator( self.geometryFromPoint(224856, 815472), crs27700 ).tenKmqlTileForNtfGrid(), 'NH20' ) #NH21
        self.assertEqual( OsTileLocator( self.geometryFromPoint(224942, 806020), crs27700 ).tenKmqlTileForNtfGrid(), 'NH20' ) #NH20

    def test_fiveKmSqTile(self):
        """Test Five Km Sq Tile"""

        self.assertEqual( OsTileLocator( self.geometryFromPoint(593091,587066), crs27700 ).fiveKmSqTile(), 'OV98NW') 
        self.assertEqual( OsTileLocator( self.geometryFromPoint(541330,120443), crs27700 ).fiveKmSqTile(), 'TQ42SW') 
        self.assertEqual( OsTileLocator( self.geometryFromPoint(358161,361649), crs27700 ).fiveKmSqTile(), 'SJ56SE') 
        self.assertEqual( OsTileLocator( self.geometryFromPoint(337914,667001), crs27700 ).fiveKmSqTile(), 'NT36NE') 

    def test_withinGB(self):
        """Test GB boundary"""

        self.assertTrue( OsTileLocator( self.geometryFromPoint(593091,587066) , crs27700 ).withinGB() )
        self.assertTrue( OsTileLocator( self.geometryFromPoint(700000,0)      , crs27700 ).withinGB() )
        self.assertTrue( OsTileLocator( self.geometryFromPoint(700000,1300000), crs27700).withinGB() )
        self.assertTrue( OsTileLocator( self.geometryFromPoint(0,1300000)     , crs27700 ).withinGB() )
        self.assertTrue( OsTileLocator( self.geometryFromPoint(0,0)           , crs27700 ).withinGB() )

        self.assertFalse( OsTileLocator( self.geometryFromPoint(-100,0)   ,crs27700).withinGB() )
        self.assertFalse( OsTileLocator( self.geometryFromPoint(-100,-100),crs27700 ).withinGB() )
        self.assertFalse( OsTileLocator( self.geometryFromPoint(0,-100)   ,crs27700).withinGB() )
        self.assertFalse( OsTileLocator( self.geometryFromPoint(100,-100) ,crs27700) .withinGB() )

    def test__otherProjections(self):
        """ Testing using alternative projections """
        crs4326 = QgsCoordinateReferenceSystem(4326)

        self.assertTrue( OsTileLocator( self.geometryFromPoint(1.0279671902, 55.1402813407) , crs4326 ).withinGB() )
        self.assertFalse( OsTileLocator( self.geometryFromPoint(-37.806420, 144.967832)   ,crs4326).withinGB() )
        self.assertEqual( OsTileLocator( self.geometryFromPoint(1.0279671902 , 55.1402813407), crs4326 ).fiveKmSqTile(), 'OV98NW') 
        self.assertEqual( OsTileLocator( self.geometryFromPoint(-5.06900313656, 57.1870488396), crs4326 ).tenKmqlTileForNtfGrid(), 'NH00' ) #NH11
        self.assertEqual( OsTileLocator( self.geometryFromPoint(-5.24175021987, 57.2753866164), crs4326 ).tenKmqlTileForNtfGrid(), 'NH02' ) #NH02
        self.assertEqual( OsTileLocator( self.geometryFromPoint(-5.067836519 , 57.275899018), crs4326 ).tenKmqlTileForNtfGrid(), 'NH02' ) #NH12
        self.assertEqual( OsTileLocator( self.geometryFromPoint(1.0279671902 , 55.1402813407), crs4326 ).tenKmSqTile(), 'OV98' )
        self.assertEqual( OsTileLocator( self.geometryFromPoint(-2.99428068739 ,55.8921196518), crs4326 ).hundredKmSqTile(), 'NT') 

    def geometryFromPoint(self, x, y):
        return QgsGeometry.fromPoint( QgsPoint(x, y) )

if __name__ == '__main__':
    unittest.main()