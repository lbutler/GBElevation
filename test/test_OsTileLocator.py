from GBElevation.models import *

import unittest

class TestOsTileLocator(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        pass

    def test_hundredKmSqTile(self):
        """Test Hundred Km Sq Tile"""

        OV = OsTileLocator(593091,587066)
        self.assertEqual( OV.hundredKmSqTile() , 'OV')

    def test_tenKmSqTile(self):
        """Test Ten Km Sq Tile"""

        OV = OsTileLocator(593091,587066)
        self.assertEqual( OV.tenKmSqTile() , 'OV98')

    def test_fiveKmSqTile(self):
        """Test Five Km Sq Tile"""

        OV = OsTileLocator(593091,587066)
        self.assertEqual( OV.fiveKmSqTile() , 'OV98NW')

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