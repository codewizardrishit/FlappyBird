import random
import sys
from unittest.main import MAIN_EXAMPLES
import pygame
from pygame.locals import *

# Global variables
FPS = 32
SCREENWIDTH = 350
SCREENHEIGHT = 690
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8  # 80% of the screen height
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.jpeg'


def welcomeScreen():
    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.1)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)


if __name__ == "__main__":
    pygame.init()  # Initializes all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Rishit")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/1.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/2.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/3.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/4.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/5.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/6.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/7.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/8.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/9.jpg').convert_alpha()
    )

GAME_SPRITES['base'] = pygame.image.load(
    'gallery/sprites/base.png').convert_alpha()
GAME_SPRITES['message'] = pygame.image.load(
    'gallery/sprites/message.png').convert_alpha()
GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
)
GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()


# Game Sounds
GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav.mp3')
GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav.mp3')
GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav.mp3')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav.mp3')
GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav.mp3')

while True:
    welcomeScreen()
    mainGame()
