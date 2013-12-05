'''
Created on Nov 2, 2013

@author: Nishad, Daniel, Tri
'''
from random import randint
from copy import deepcopy
from math import pow
from piece import *

class Board(object):
    HEIGHT = 22
    WIDTH = 12
    
    def __init__(self):
        self.queue = []
        for i in range(0,5):
            self.queue.append(Piece(randint(0,6),0))
        self.hold = 0
        self.board = [[False]*(self.WIDTH) for x in range(self.HEIGHT)]
        # setting default to white is fallback
        self.colors = [[WHITE_COLOR]*(self.WIDTH) for x in range(self.HEIGHT)]
        
        #Change the leftmost and rightmost columns to true
        for i in range(self.HEIGHT):
            self.board[i][0] = True
            self.board[i][self.WIDTH-1] = True
        
        #Change the bottom row to True
        for j in range(self.WIDTH):
            self.board[self.HEIGHT-1][j] = True
        
        self.xActive = 0
        self.yActive = 0
        self.isGameOver = False
        self.active = None
        self.score = 0

        self.timer = 1

    def canMove(self, xShift, yShift):
        array = self.active.get()
        for i in range(4):
            for j in range(4):
                if(array[i][j]):
                    xOnBoard = self.yActive + i + yShift
                    yOnBoard = self.xActive + j + xShift
                    if(self.board[xOnBoard][yOnBoard]):
                        return False
        return True
    
    def move(self, xShift, yShift): #Returns whether or not the piece was moved
        if(self.canMove(xShift, yShift)):
            self.xActive += xShift
            self.yActive += yShift
            return True
        else:
            if(xShift==0 and yShift==1):
                self.merge()
                self.checkLineFull()  #Clears full lines
                self.createNewPiece()
                self.isGameOver = not self.canMove(0,0)
            return False    

    def createNewPiece(self):
        shape = randint(0,6)
        orientation = 0
        self.active = self.queue.pop(0)
        self.queue.append(Piece(shape,orientation))
        self.yActive = 0
        self.xActive = 4
        self.timer = pow(0.985, int(self.score/ 90))

    def addPiece(self, piece):
        self.active = (piece)
        self.yActive = 0
        self.xActive = 4

    def dropPiece(self):
        while self.move(0,1):
            pass

    def moveShadow(self, xShift, yShift): #Only for shadow piece use
        if(self.canMove(xShift, yShift)):
            self.xActive += xShift
            self.yActive += yShift
            return True
        else:
            if(xShift==0 and yShift==1):
                self.merge()
            return False

    def dropShadowPiece(self):   #This is soley for the shadow piece
        while (self.moveShadow(0,1)):
            pass

    def merge(self):
        activeArray = self.active.get()
        for i in range(4):
            for j in range(4):
                x = min(self.HEIGHT-1, self.yActive + i)
                y = min(self.WIDTH-1, self.xActive + j)
                self.board[x][y] = self.board[x][y] or activeArray[i][j]
                if activeArray[i][j]:
                    self.colors[x][y] = self.active.color  # adds color to array

    def canRotate(self,n):
        ghost = deepcopy(self.active)   
        ghost.rotate(n)
        ghostArray = ghost.get()
        for i in range(4):
            for j in range(4):
                if(ghostArray[i][j]):
                    xOnBoard = self.yActive + i
                    yOnBoard = self.xActive + j
                    if(xOnBoard>=self.WIDTH or yOnBoard>=self.HEIGHT or self.board[xOnBoard][yOnBoard]==True):
                        return False
        return True
    
    def rotate(self,n): 
        #Since it can't be rotated in place, we move it closer to the horizontal center and try to move it there.
        ghost = deepcopy(self)

        
        ghost.active.rotate(1)
        
        if not (ghost.canMove(0,0)): #its a vlaid rotation
            #This checks to see if the piece needs to be moved up
            a = ghost.move(1, 0) 
            b = ghost.move(-1,0)
            c = ghost.move(-1,0) 
            d = ghost.move(1, 0)
            if(a or b or c or d):   #!!!!DO NOT OPTIMIZE THIS FURTHER. DOING SO WOULD INTRODUCT SHORT-CIRCUIT EVALUATION
                self = ghost
            else:
                if(not ghost.move(0,-1)):
                    return None
        
        #Copy ghost into self
        self.board = ghost.board
        self.active = ghost.active
        self.xActive = ghost.xActive
        self.yActive = ghost.yActive

    def checkLineFull(self):     
        list = []
        for x in range(0,self.HEIGHT-1):
            tmp = True
            for y in range(1,self.WIDTH-1):
                # either option works below
                #if self.board[x][y] == False:
                #    tmp = False
                tmp = tmp and self.board[x][y]
            if tmp:
                list.append(x)
        for i in range(0,len(list)):
            self.clearLine(list[i])

        # score manipulation
        if len(list) == 4:
            self.score = self.score + 4*100 + 150
        else:
            self.score = self.score + len(list)*100
        

    def clearLine(self,n):
        tmp = deepcopy(self.board)
        for x in range(1,n+1):
            for y in range(1,self.WIDTH-1):
                self.board[x][y] = tmp[x-1][y]

    def getPieceOnBoard(self):  # this returns a blank board with only the active piece
        re = Board()
        re.addPiece(self.active)
        re.xActive = self.xActive
        re.yActive = self.yActive
        re.merge()
        return re.board
    
    def getPieceColorOnBoard(self):
        re = Board()
        re.addPiece(self.active)
        re.xActive = self.xActive
        re.yActive = self.yActive
        re.merge()
        return re.colors
    
    def getShadow(self):
        # this code could be replaced by otherDeep = deepcopy(self)
        otherDeep = Board()
        otherDeep.board = deepcopy(self.board)
        otherDeep.addPiece(self.active)
        otherDeep.xActive = self.xActive
        #otherDeep.yActive = self.yActive
        otherDeep.dropShadowPiece()
        reBoard = [[False]*(self.WIDTH) for x in range(self.HEIGHT)]
        for x in range(0,self.WIDTH):
            for y in range(0,self.HEIGHT):
                if otherDeep.board[y][x] != self.board[y][x]:
                    reBoard[y][x] = True    
        return reBoard

    def holdPiece(self):
        if self.hold == 0:
            self.hold = self.active
            self.active = self.queue.pop(0)
            self.queue.append(Piece(randint(0,6),0))
        else:
            tmp = self.active
            self.active = self.hold
            self.hold = tmp 
        self.xActive = 4
        self.yActive = 0
# PROBLEMS WE ENCOUNTERED
# we actually had to add yActive to i and not to j
# we originally had canMove and moveLR and canRotate and rotate...
    #but we should change this to one rotate function that returns the same piece if it cannot be rotated
    #or the correctly rotated piece if it *can* be rotated
#we created two methods, one that returns the board w/o the piece and one that returns the piece without the board, but then we just merged them into one getCurrentBoard method
#instead of creating four different canMove methods, make one method that takes two arguments (a left/right shift and an up/down shift) and return whether or not the piece can be moved there
#instead of checking invalid indices on the board array, we instead made the borders of the board array equal to True and saved some inequality checking/testing
#if a piece cannot be rotated, we tried shifting the piece and then rotating it.
    #first we had to prioritize whether the piece should move horiz or vert versus the other
    #then if a piece can be moved and then rotated, that's different than rotating a piece and then rotating i
    #we tried saying horiz takes priority. so move the piece left or right (towards or away from center?) and then up and down
    #but what if the piece is the only piece on the board & its at the bottom of the screen. then rotating it shouldnt shift it horizontally, it sohuld shift it up, so in this case, vertical shifting takes priority
