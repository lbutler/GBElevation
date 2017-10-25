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