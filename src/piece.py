# tetris/piece.py
import pygame
from .setting import *

class Piece:
    def __init__(self, shape_index, x=GRID_WIDTH // 2 - 1, y=0):
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.x = x
        self.y = y
        self.rotation = 0
    
    def rotate(self):
           rows = len(self.shape)
        cols = len(self.shape[0])
        rotate = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for r in range(rows):
            for c in range(cols):
                rotate[c][rows - 1 - r] = self.shape[r][c]
        
        self.shape = rotate
    
    
    def draw(self, screen):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (self.x + x) * GRID_SIZE,
                        (self.y + y) * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE
                    )
                    pygame.draw.rect(screen, self.color, rect,0,4)
                    pygame.draw.rect(screen, WHITE, rect, 2,4)