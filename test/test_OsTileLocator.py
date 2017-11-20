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

import unittest

class TestOsTileLocator(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        pass

    def test_hundredKmSqTile(self):
        """Test Hundred Km Sq Tile"""

        self.assertEqual( OsTileLocator(541330,120443).hundredKmSqTile(), 'TQ') 
        OV = OsTileLocator(593091,587066)
        self.assertEqual( OV.hundredKmSqTile() , 'OV')
        self.assertEqual( OsTileLocator(593091,587066).hundredKmSqTile() , 'OV')
        self.assertEqual( OsTileLocator(358161,361649).hundredKmSqTile(), 'SJ') 
        self.assertEqual( OsTileLocator(337914,667001).hundredKmSqTile(), 'NT') 

    def test_tenKmSqTile(self):
        """Test Ten Km Sq Tile"""

        OV = OsTileLocator(593091,587066)
        self.assertEqual( OV.tenKmSqTile() , 'OV98')

    def test_tenKmqlTileForNtfGrid(self):
        """Test Ten Km Sq Tile for Ntf grid file"""
        self.assertEqual( OsTileLocator(205609, 807137).tenKmqlTileForNtfGrid(), 'NH00' ) #NH00
        self.assertEqual( OsTileLocator(214717, 807395).tenKmqlTileForNtfGrid(), 'NH00' ) #NH10
        self.assertEqual( OsTileLocator(205265, 814784).tenKmqlTileForNtfGrid(), 'NH00' ) #NH01
        self.assertEqual( OsTileLocator(214631, 814870).tenKmqlTileForNtfGrid(), 'NH00' ) #NH11
        self.assertEqual( OsTileLocator(204664, 825181).tenKmqlTileForNtfGrid(), 'NH02' ) #NH02
        self.assertEqual( OsTileLocator(215147, 824752).tenKmqlTileForNtfGrid(), 'NH02' ) #NH12
        self.assertEqual( OsTileLocator(224684, 824838).tenKmqlTileForNtfGrid(), 'NH22' ) #NH22
        self.assertEqual( OsTileLocator(224856, 815472).tenKmqlTileForNtfGrid(), 'NH20' ) #NH21
        self.assertEqual( OsTileLocator(224942, 806020).tenKmqlTileForNtfGrid(), 'NH20' ) #NH20

    def test_fiveKmSqTile(self):
        """Test Five Km Sq Tile"""

        OV = OsTileLocator(593091,587066)
        self.assertEqual( OV.fiveKmSqTile() , 'OV98NW')
        self.assertEqual( OsTileLocator(541330,120443).fiveKmSqTile(), 'TQ42SW') 
        self.assertEqual( OsTileLocator(358161,361649).fiveKmSqTile(), 'SJ56SE') 
        self.assertEqual( OsTileLocator(337914,667001).fiveKmSqTile(), 'NT36NE') 

    def test_withinGB(self):
        """Test GB boundary"""

        self.assertTrue( OsTileLocator(593091,587066).withinGB() )
        self.assertTrue( OsTileLocator(700000,0).withinGB() )
        self.assertTrue( OsTileLocator(700000,1300000).withinGB() )
        self.assertTrue( OsTileLocator(0,1300000).withinGB() )
        self.assertTrue( OsTileLocator(0,0).withinGB() )

        self.assertFalse( OsTileLocator(-100,0).withinGB() )
        self.assertFalse( OsTileLocator(-100,-100).withinGB() )
        self.assertFalse( OsTileLocator(0,-100).withinGB() )
        self.assertFalse( OsTileLocator(100,-100).withinGB() )

if __name__ == '__main__':
    unittest.main()