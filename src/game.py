import pygame
from .setting import *
from .board import Board
from .util import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.path_font = "assets/font/Rubik-Bold.ttf"
        self.path_sound = "assets/sound/move_sound.wav"
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.running = True

    def soundEffect(self):
        sound = loadSound(self.path_sound)
        sound.stop()
        sound.play()

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if not self.board.game_over:
                if event.type == pygame.KEYDOWN:
                    self.soundEffect()
                    if event.key == pygame.K_LEFT:
                        self.pieceMove(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pieceMove(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.pieceMove(0, 1)
                    elif event.key == pygame.K_UP:
                        self.pieceRotate()
                    elif event.key == pygame.K_SPACE:
                        self.instanDrop()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.board.game_over:
                    self.board = Board()
    
    def pieceMove(self, dx, dy):
        if self.board.validPosition(x=self.board.current_piece.x + dx, y=self.board.current_piece.y + dy):
            self.board.current_piece.x += dx
            self.board.current_piece.y += dy
            return True
        return False
    

    def pieceRotate(self):
        shape = self.board.current_piece.shape
        self.board.current_piece.rotate()
        if not self.board.validPosition():
            self.board.current_piece.shape = shape
    
    def instanDrop(self):
        while self.pieceMove(0, 1):
            pass
        self.board.placePiece()
    
    def update(self):
        if self.board.game_over:
            return
            
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.board.drop_time > self.board.drop_speed:
            if not self.pieceMove(0, 1):
                self.board.placePiece()
            self.board.drop_time = current_time
    
    def draw(self):
        self.screen.fill(PURPLE)
        self.board.draw(self.screen)
        
        if self.board.game_over:
            self.drawGameOver()
        
        pygame.display.flip()
    
    
    def drawGameOver(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font = loadFont(self.path_font,60)
        text = font.render("GAME OVER", True, RED)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, rect)
        
        second_font = loadFont(self.path_font,25)
        score_text = second_font.render(f"Final Score: {self.board.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        restart_text = second_font.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        while self.running:
            self.eventHandler()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()