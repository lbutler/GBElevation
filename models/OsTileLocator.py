# -*- coding: utf-8 -*-
import math

class OsTileLocator:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = \
        [['V','W','X','Y','Z'], \
        ['Q','R','S','T','U'], \
        ['L','M','N','O','P'], \
        ['F','G','H','J','K'], \
        ['A','B','C','D','E']]

    def hundredKmSqTile(self):

        # False Origin of Grid 0,0 starts at Letter S
        # offset by 1,2 on grid lookup to start on this letter
        firstLetterX = math.trunc( self.x / 500000) + 1
        firstLetterY = math.trunc( self.y / 500000) + 2

        secondLetterX = math.trunc( (self.x % 500000) / 100000)
        secondLetterY = math.trunc( (self.y % 500000) / 100000)      

        firstLetter = self.grid[firstLetterX][firstLetterY]
        secondLetter = self.grid[secondLetterX][secondLetterY]

        return firstLetter + secondLetter


    def tenKmSqTile(self):

        firstNumber = math.trunc( (self.x % 100000) / 10000 )
        secondNumber = math.trunc( (self.y % 100000) / 10000 )

        tenKmSqTile = self.hundredKmSqTile() + str(firstNumber) + str(secondNumber)

        return tenKmSqTile


    def fiveKmSqTile(self):

        if self.y % 10000 > 5000:
            NorthOrSouth = "N"
        else:
            NorthOrSouth = "S"

        if self.x % 10000 > 5000:
            WestOrEast = "E"
        else:
            WestOrEast = "W" 

        fiveKmSqTile = self.tenKmSqTile() + NorthOrSouth + WestOrEast

        return fiveKmSqTile


    def withinGB(self):
        if self.x >= 0 and self.x <=700000 and self.y >= 0 and self.y <=1300000:
            return True
        else:
            return False
