import pygame

def loadSound(path):
    return pygame.mixer.Sound(path)

def loadFont(path,size):
    return pygame.font.Font(path,size)
