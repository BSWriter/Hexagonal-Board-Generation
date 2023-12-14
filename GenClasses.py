import math
import random
import json

class Board:
    def __init__(self, rows, cols, pSize, surrWall):
        self.rows = rows
        self.cols = cols
        self.pSize = pSize
        self.panels = []
        self.walls = surrWall

        self.create_Board()
    
    def create_Board(self):
        panels = []
        pSize = self.pSize
        radi = pSize / 2
        for r in range(self.rows):
            for c in range(self.cols):
                yoffset = 0
                xoffset = 0
                
                yPos = (r * pSize)
                xPos = (c * pSize)
                yoffset = ((radi - radi * math.sin(math.radians(60))) * (yPos / pSize)) * 2
                yPos -= yoffset
                xoffset = ((radi - radi * math.cos(math.radians(60))) * (xPos / pSize))
                xPos -= xoffset

                if c % 2 == 1:
                    yPos += pSize / 2 - (radi - radi * math.sin(math.radians(60)))

                p = Panel(xPos, yPos, pSize)
                p.setGridPos((c,r))
                # Set the surrounding panels using the rows and cols limit as context
                p.flagSurrondingTiles(self.rows, self.cols)
                # If the panel is at the sides of the board, make it a wall
                if (self.walls) and (r == 0 or c == 0 or r == self.rows-1 or c == self.cols-1):
                    p.label = 4
                panels.append(p)
        self.panels = panels
    
    def getPanels(self):
        return self.panels
    
    def setPanels(self, panels):
        self.panels = panels
    
    def getDict(self):
        res = {"rows": self.rows, "cols": self.cols, "panel size": self.pSize, "panels": []}
        for panel in self.panels:
            res["panels"].append(panel.getDict())
        return res
    
    

class Panel:
    def __init__(self, xPos, yPos, size):
        r = size / 2

        self.center = (xPos, yPos)
        self.label = random.choice([1,2,3])
        self.gridPos = (None, None)
        self.surroundingPanels = []
        self.elevation = 1
        self.p1 = (xPos + r * math.cos(math.radians(0)), yPos + r * math.sin(math.radians(0)))
        self.p2 = (xPos + r * math.cos(math.radians(60)), yPos + r * math.sin(math.radians(60)))
        self.p3 = (xPos + r * math.cos(math.radians(120)), yPos + r * math.sin(math.radians(120)))
        self.p4 = (xPos + r * math.cos(math.radians(180)), yPos + r * math.sin(math.radians(180)))
        self.p5 = (xPos + r * math.cos(math.radians(240)), yPos + r * math.sin(math.radians(240)))
        self.p6 = (xPos + r * math.cos(math.radians(300)), yPos + r * math.sin(math.radians(300)))

    def getCoordinates(self):
        return [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]

    def coordinateList(self):
        return [self.p1[0], self.p1[1], self.p2[0], self.p2[1], self.p3[0], self.p3[1],
                self.p4[0], self.p4[1], self.p5[0], self.p5[1], self.p6[0], self.p6[1]]
    
    def getCenter(self):
        return self.center
    
    def setCenter(self, newCenter):
        self.center = newCenter
    
    def getLabel(self):
        return self.label
    
    def setLabel(self, newLabel, maxLabel):
        altLabel = newLabel
        if altLabel > maxLabel:
            altLabel = 0

        self.label = altLabel

    def getGridPos(self):
        return self.gridPos
    
    def setGridPos(self, posIn):
        self.gridPos = posIn
    
    def getSurroundingPanels(self):
        return self.surroundingPanels

    def setSurroundingPanels(self, panelsIn):
        self.surroundingPanels = panelsIn

    def flagSurrondingTiles(self, maxRows, maxCols):
        x = self.gridPos[0]
        y = self.gridPos[1]

        surroundingTiles = []
        if x % 2 == 0:
            surroundingTiles = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x, y+1), (x+1, y)]
        else:
            surroundingTiles = [(x-1, y), (x, y-1), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]

        # Remove any extra positions from surroundingTiles (locations that do not have a corresponding panel)
        resPanels = []
        for loc in surroundingTiles:
            if loc[0] >= 0 and loc[0] < maxCols and loc[1] >= 0 and loc[1] < maxRows:
                resPanels.append(loc)

        self.surroundingPanels = resPanels
    
    def getElevation(self):
        return self.elevation
    
    def incrementElevation(self):
        self.elevation += 1
    
    def decrementElevation(self):
        self.elevation -= 1

    def getDict(self):
        # res = {"grid position": self.gridPos, "label":self.label, "center":self.center, "coordinates":self.getCoordinates()}
        res = {"grid position": self.gridPos, "label":self.label, "center":self.center, "elevation":self.elevation, "surrounding":self.surroundingPanels}
        return res




