# some constants
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
GREY_COLOR = (192,192,192)
GREEN_COLOR = (51,255,102)
RED_COLOR = (176,0,0)
PURPLE_COLOR = (200,0,200)
BLUE_COLOR = (0,0,200)
YELLOW_COLOR = (200,200,0)
PINK_COLOR = (255,105,180)

class Piece(object):
    PIECES = [[[[False,False,False,False],  #L-piece
           [False,True,False,False],
           [False,True,False,False],
           [False,True,True,False]],

          [[False,False,False,False],  #90 degrees
               [False,False,False,False],
           [True,True,True,False],
           [True,False,False,False]],

          [[False,False,False,False],  #180 degrees
               [True,True,False,False],
           [False,True,False,False],
           [False,True,False,False]],

          [[False,False,False,False],  #270 degrees
               [False,False,True,False],
           [True,True,True,False],
           [False,False,False,False]]],
        
         [[[False,False,False,False],  #T-piece
          [False,True,False,False],
          [True,True,True,False],
          [False,False,False,False]],
          
         [[False,False,False,False],  
              [False,True,False,False],
          [False,True,True,False],
          [False,True,False,False]],

         [[False,False,False,False],
              [False,False,False,False],
          [True,True,True,False],
          [False,True,False,False]],

         [[False,False,False,False],
              [False,True,False,False],
          [True,True,False,False],
          [False,True,False,False]]],

         [[[False,False,False,False],  #I-piece
              [False,False,False,False],
          [True,True,True,True],
          [False,False,False,False]],

                 [[False,False,True,False],
          [False,False,True,False],
          [False,False,True,False],
          [False,False,True,False]],

             [[False,False,False,False],
          [False,False,False,False],
          [True,True,True,True],
          [False,False,False,False]],

         [[False,False,True,False],
          [False,False,True,False],
          [False,False,True,False],
          [False,False,True,False]]],

                 [[[False,False,False,False],  #Z-piece
          [False,False,False,False],
          [True,True,False,False],
          [False,True,True,False]],

        [[False,False,False,False],
         [False,False,True,False],
         [False,True,True,False],
         [False,True,False,False]],

         [[False,False,False,False],  
          [False,False,False,False],
          [True,True,False,False],
          [False,True,True,False]],

        [[False,False,False,False],
         [False,False,True,False],
         [False,True,True,False],
         [False,True,False,False]]],
        
        [[[False,False,False,False],  #S-Piece
          [False,False,False,False],
          [False,True,True,False],
          [True,True,False,False]],

         [[False,False,False,False],
          [False,True,False,False],
          [False,True,True,False],
          [False,False,True,False]],

         [[False,False,False,False],  
          [False,False,False,False],
          [False,True,True,False],
          [True,True,False,False]],

         [[False,False,False,False],
          [False,True,False,False],
          [False,True,True,False],
          [False,False,True,False]]],

         [[[False,False,False,False],  #L-prime-piece
           [False,True,False,False],
           [False,True,False,False],
           [True,True,False,False]],

          [[False,False,False,False],
           [True,False,False,False],
           [True,True,True,False],
           [False,False,False,False]],

          [[False,False,False,False],
           [False,True,True,False],
           [False,True,False,False],
           [False,True,False,False]],

          [[False,False,False,False],
           [False,False,False,False],
           [True,True,True,False],
           [False,False,True,False]]],

         [[[False,False,False,False], #O-piece
               [False,True,True,False],
           [False,True,True,False],
           [False,False,False,False]],

          [[False,False,False,False], 
               [False,True,True,False],
           [False,True,True,False],
           [False,False,False,False]],

          [[False,False,False,False], 
               [False,True,True,False],
           [False,True,True,False],
           [False,False,False,False]],

          [[False,False,False,False], 
               [False,True,True,False],
           [False,True,True,False],
           [False,False,False,False]]]]

    def __init__(self, piece, orientation):
        self.orientation = orientation
        self.piece = piece  #pieces numbers are between 0 and 6, inclusive

        if self.piece == 0:      # ugly way for determining piece color
            self.color = GREY_COLOR
        elif self.piece == 1:
            self.color = GREEN_COLOR
        elif self.piece == 2:
            self.color = RED_COLOR
        elif self.piece == 3:
            self.color = PURPLE_COLOR
        elif self.piece == 4:
            self.color = BLUE_COLOR
        elif self.piece == 5:
            self.color = YELLOW_COLOR
        elif self.piece == 6:
            self.color = PINK_COLOR
    
    def __init(self, otherBoard):
        self = deepcopy(otherBoard)
        
    def rotate(self,num):
        self.orientation = (self.orientation + num ) % 4 # Beware: (-41) % 3 == -2 in C, but (-41) % 3 == 1 in Python
            
    def get(self):
        return self.PIECES[self.piece][self.orientation]
        
    def printPiece(self):
        for i in range(0, 4):
            print("".join(['-' if not x else 'X' for x in self.PIECES[self.piece][self.orientation][i]]))
