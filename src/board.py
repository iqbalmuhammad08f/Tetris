# tetris/board.py
import pygame
import random
from .setting import *
from .piece import Piece
from .util import *

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.newPiece()
        self.next_piece = self.newPiece()
        self.path_font = "assets/font/Rubik-Bold.ttf"
        self.path_sound = "assets\sound\score_sound.wav"
        self.game_over = False
        self.score = 0
        self.level = 1
        self.drop_speed = DROP_SPEED
        self.drop_time = 0
    
    def newPiece(self):
        return Piece(random.randint(0, len(SHAPES) - 1))
    
    def soundEffect(self):
        sound = loadSound(self.path_sound)
        sound.play()
    
    def validPosition(self, piece=None, x=None, y=None):
        if piece is None:
            piece = self.current_piece
        if x is None:
            x = piece.x
        if y is None:
            y = piece.y
            
        for r, row in enumerate(piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    if (x + c < 0 or x + c >= GRID_WIDTH or 
                        y + r >= GRID_HEIGHT or 
                        (y + r >= 0 and self.grid[y + r][x + c])):
                        return False
        return True
    
    def placePiece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, cell in enumerate(row):
                if cell and self.current_piece.y + r >= 0:
                    self.grid[self.current_piece.y + r][self.current_piece.x + c] = self.current_piece.color
        
        self.clearLine()
        
        if not self.game_over:
            self.current_piece = self.next_piece
            self.next_piece = self.newPiece()
            
            if not self.validPosition():
                self.game_over = True
    
    def clearLine(self):
        lines_clear = 0
        for r in range(GRID_HEIGHT):
            if all(self.grid[r]):
                lines_clear += 1
                for r2 in range(r, 0, -1):
                    self.grid[r2] = self.grid[r2-1][:]
                self.grid[0] = [0 for _ in range(GRID_WIDTH)]
        
        if lines_clear > 0:
            self.soundEffect()
            self.score += self.calculateScore(lines_clear)
            self.updateLevel()
    
    def calculateScore(self, line):
        return {1: 100, 2: 300, 3: 500, 4: 800}[line] * self.level
    
    def updateLevel(self):
        self.level = self.score // 2000 + 1
        self.drop_speed = DROP_SPEED * (SPEED_INCREASE ** (self.level - 1))
    
    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    x * GRID_SIZE,
                    y * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                color = self.grid[y][x] if self.grid[y][x] else BLACK
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)
                pygame.draw.rect(screen, GRAY, rect, 2, 4)
        
        if not self.game_over:
            self.current_piece.draw(screen)
        
        self.drawSidebar(screen)
    
    def drawSidebar(self, screen):
        sidebar_x = GRID_WIDTH * GRID_SIZE

        title_font = loadFont(self.path_font,50)
        title = title_font.render("Tetris", True, WHITE)
        screen.blit(title, (sidebar_x + 20, 10))

        font = loadFont(self.path_font,25)
        text = font.render("Next:", True, WHITE)
        screen.blit(text, (sidebar_x + 20, 100))
        
        next_piece_x = sidebar_x + (SIDEBAR_WIDTH - len(self.next_piece.shape[0]) * GRID_SIZE) // 2
        next_piece_y = 150
        
        for r, row in enumerate(self.next_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        next_piece_x + c * GRID_SIZE,
                        next_piece_y + r * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE
                    )
                    pygame.draw.rect(screen, self.next_piece.color, rect,0,4)
                    pygame.draw.rect(screen, WHITE, rect, 2,4)
        
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (sidebar_x + 20, 250))
        
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (sidebar_x + 20, 300))