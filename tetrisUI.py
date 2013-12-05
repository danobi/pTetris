#!/usr/bin/python
from math import pow
import pygame, sys
import random
import time
from pygame.locals import *
from tetris import *
 
pygame.init()
board = Board()
 
# constants
X_WINDOW = 450
Y_WINDOW = 600
X_TETRIS_WINDOW = int(X_WINDOW - X_WINDOW/3) # x-region for active tetris board
BOX_SIZE = int((X_WINDOW - X_WINDOW/3)/10)  # the width/height of each tetris square
SMALL_SIZE = BOX_SIZE / 2
QUEUE_X = 350
QUEUE_Y = 200

# some helper methods
def newRandomPiece():
    return Piece(random.randint(0,6),random.randint(0,3))
def writeText(score):
   font=pygame.font.Font(None,30)
   scoretext=font.render(str(score), 1,(255,255,255))
   screen.blit(scoretext, (320,20)) 

# initialization stuff
screen = pygame.display.set_mode([X_WINDOW,Y_WINDOW])
screen.fill(WHITE_COLOR)
mainloop,fps =  True,30
Clock = pygame.time.Clock()
timeToWait = 1  # this should be changed based on current difficulty
board.addPiece(newRandomPiece())
pieceTime = time.clock()   # microseconds since time.clock() was first called
waitDuration = 1  # this changes to some other value if game is paused


while mainloop:
    tickFPS = Clock.tick(fps)
    pygame.display.set_caption("pTetris FPS: %.2f" % (Clock.get_fps()))  # title and fps count
    screen.fill(BLACK_COLOR)
    pygame.draw.line(screen,WHITE_COLOR,(X_TETRIS_WINDOW,0),(X_TETRIS_WINDOW,Y_WINDOW),4) #game divider 
    
    # drawing the pieces
    shadowPiece = board.getShadow()
    for y in range(1,len(board.board[0])-1):  # ignores extra side bits
        for x in range(1,len(board.board)-1):  # ditto
            if board.board[x][y]  == True:
                pygame.draw.rect(screen,board.colors[x][y],pygame.Rect((y-1)*BOX_SIZE,(x-1)*BOX_SIZE,BOX_SIZE,BOX_SIZE))
            if shadowPiece[x][y] == True:
                pygame.draw.rect(screen,GREY_COLOR,pygame.Rect((y-1)*BOX_SIZE,(x-1)*BOX_SIZE,BOX_SIZE,BOX_SIZE))
                pygame.draw.rect(screen,BLACK_COLOR,pygame.Rect((y-1)*BOX_SIZE+5,(x-1)*BOX_SIZE+5,BOX_SIZE-10,BOX_SIZE-10))
            if board.getPieceOnBoard()[x][y] == True:
                pygame.draw.rect(screen,board.getPieceColorOnBoard()[x][y],pygame.Rect((y-1)*BOX_SIZE,(x-1)*BOX_SIZE,BOX_SIZE,BOX_SIZE))

    # drawing the tetris grid
    for x in range(0,X_TETRIS_WINDOW,30): 
        for y in range(0,Y_WINDOW,30):
            pygame.draw.line(screen,BLACK_COLOR,(x,0),(x,Y_WINDOW))
            pygame.draw.line(screen,BLACK_COLOR,(0,y),(X_TETRIS_WINDOW,y))

    # drawing text onto screen
    writeText("Score: " + str(board.score))
    
    # drawing the queue pieces
    for p in range(0,5):
        arr = board.queue[p].get()
        for i in range(0,4):
            for j in range(0,4):
                if arr[i][j] == True:
                    pygame.draw.rect(screen,WHITE_COLOR,pygame.Rect(QUEUE_X + j*SMALL_SIZE,QUEUE_Y + 50*p + i*SMALL_SIZE,SMALL_SIZE,SMALL_SIZE))

    # drawing the hold piece
    if not board.hold == 0:
        for i in range(0,4):
            for j in range(0,4):
                if board.hold.get()[i][j] == True:
                    pygame.draw.rect(screen,RED_COLOR,pygame.Rect(QUEUE_X + j*SMALL_SIZE,75 + i*SMALL_SIZE,SMALL_SIZE,SMALL_SIZE))

    # Key event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # for quitting
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # ditto
                mainloop = False
            elif event.key == pygame.K_q:
                mainloop = False
            elif event.key == pygame.K_LEFT:
                board.move(-1,0)
                shadowPiece = board.getShadow()
            elif event.key == pygame.K_RIGHT:
                board.move(1,0)
                shadowPiece = board.getShadow()
            elif event.key == pygame.K_DOWN:
                board.move(0,1)
            elif event.key == pygame.K_SPACE:
                board.dropPiece()
            elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                board.holdPiece()
            elif event.key == pygame.K_UP or event.key == pygame.K_z:
                board.rotate(1)
            elif event.key == pygame.K_x:
                board.rotate(-1)
            # pause is broken --> functionality temporarily removed from game
            elif event.key == pygame.K_p:
                if waitDuration == 100000000:
                    waitDuration = board.timer #= pow(.9,int(board.score/90))
                else:
                    waitDuration = 100000000 # this is a hacky solution, it just 
                                            # waits for that long in seconds
            elif event.key == pygame.K_r:
                board = Board()
                board.addPiece(newRandomPiece())
    
    # drop timer
    if time.clock() - pieceTime > board.timer:
        board.move(0,1)
        pieceTime = time.clock()

    pygame.display.flip()
    #pygame.display.update(updatedRects)

    # checks if game top has been reached
    if board.isGameOver:
        mainloop = False
 
pygame.quit() # idle friendly 


###### LIST OF PROBLEMS #######
# low framerate -> use double buffered solution
# did not know how to extend class -> used from _ import *
# all the pieces on the board have the same color -> created a seperate 2d array for colors values and a new method in piece class for color
# grid was not showing over the pieces -> changed order of render
# active piece color was not displaying correctly -> the line that rendered colors was not calling the active piece colors
# shadow piece was not displaying correctly -> had to make a deep copy of current board and then use an XOR check to find the temporarily dropped piece
# dropping pieces was not working -> made two seperate methods to handle checking if a line was full and clearing one line at a time
# shadow piece and line clear wasn't playing nice together -> had to make duplicate drop and move methods that would not create a new piece or check if lines were full
# we were getting massive framerate lag after implementing score calculation -> reduced score calculation to once per new piece creation
