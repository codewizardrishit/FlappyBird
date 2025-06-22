import random
import sys
from unittest.main import MAIN_EXAMPLES
import pygame
from pygame.locals import *

# Global variables
FPS = 32
SCREENWIDTH = 350
SCREENHEIGHT = 630
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.85  
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
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+SCREENWIDTH/2, 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+SCREENWIDTH/2, 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccV = -8  # velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # Score Check
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score += 1
                print(f"Your score is : {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if pipe out of screen , remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        DIGIT_WIDTH = 30   
        DIGIT_HEIGHT = 40
        width = len(myDigits) * DIGIT_WIDTH
        
        

        Xoffset = (SCREENWIDTH-width)/2
        tempX = Xoffset
        for digit in myDigits:
            scaled_digit = pygame.transform.scale(GAME_SPRITES['numbers'][digit],(DIGIT_WIDTH,DIGIT_HEIGHT))
            SCREEN.blit(scaled_digit,(tempX, SCREENHEIGHT*0.12))
            tempX += DIGIT_WIDTH
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery>GROUNDY -30 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()

    for pipe in upperPipes:
        if (playery < (pipeHeight+pipe['y']) and abs(playerx-pipe['x']) <GAME_SPRITES['pipe'][0].get_width()) :
            GAME_SOUNDS['hit'].play()
            return True    

    for pipe in lowerPipes :
        if (playery + GAME_SPRITES['player'].get_height()> pipe['y'] and abs(playerx-pipe['x']) <GAME_SPRITES['pipe'][0].get_width()) :
            GAME_SOUNDS['hit'].play()
            return True
    return False 

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    baseHeight = GAME_SPRITES['base'].get_height()

    gap = int(SCREENHEIGHT / 3.8)  # Reasonable gap between pipes
    pipeX = SCREENWIDTH + 10

    # Set limits for the Y of the upper pipe (top pipe should not come too low)
    upperY_min = -pipeHeight + 100  # pipe can be this low at max (i.e., 100 px from top)
    upperY_max = -pipeHeight + 200  # pipe stays within top quarter of screen

    y1 = random.randint(upperY_min, upperY_max)  # upper pipe Y (always negative)
    y2 = y1 + pipeHeight + gap  # lower pipe Y, based on upper pipe and gap

    pipe = [
        {'x': pipeX, 'y': y1},  # Upper pipe
        {'x': pipeX, 'y': y2}   # Lower pipe
    ]
    return pipe

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
