# import random
# import sys
# import pygame
# from pygame.locals import *

# # Game Constants
# FPS = 32
# SCREENWIDTH = 289
# SCREENHEIGHT = 511
# SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
# GROUNDY = SCREENHEIGHT * 0.8
# GAME_SPRITES = {}
# GAME_SOUNDS = {}
# PLAYER = 'gallery/sprites/bird.png'
# BACKGROUND = 'gallery/sprites/bg.png'  # updated
# PIPE = 'gallery/sprites/pillar.png'     # changed from pipe.png
# BIRD_SCALE = 0.12  # scale bird image

# def welcomeScreen():
#     playerx = int(SCREENWIDTH / 5)
#     playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
#     messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
#     messagey = int(SCREENHEIGHT * 0.13)
#     basex = 0

#     while True:
#         for event in pygame.event.get():
#             if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
#                 return
#         SCREEN.blit(GAME_SPRITES['background'], (0, 0))
#         SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
#         SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
#         SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
#         pygame.display.update()
#         FPSCLOCK.tick(FPS)


# def mainGame():
#     score = 0
#     playerx = int(SCREENWIDTH / 5)
#     playery = int(SCREENHEIGHT / 2)
#     basex = 0

#     newPipe1 = getRandomPipe()
#     newPipe2 = getRandomPipe()

#     upperPipes = [
#         {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
#         {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
#     ]
#     lowerPipes = [
#         {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
#         {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
#     ]

#     pipeVelX = -4
#     playerVelY = -9
#     playerMaxVelY = 10
#     playerAccY = 1
#     playerFlapAccv = -8
#     playerFlapped = False

#     while True:
#         for event in pygame.event.get():
#             if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
#                 if playery > 0:
#                     playerVelY = playerFlapAccv
#                     playerFlapped = True
#                     GAME_SOUNDS['wing'].play()

#         if isCollide(playerx, playery, upperPipes, lowerPipes):
#             GAME_SOUNDS['die'].play()
#             return

#         playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
#         for pipe in upperPipes:
#             pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
#             if pipeMidPos <= playerMidPos < pipeMidPos + 4:
#                 score += 1
#                 GAME_SOUNDS['point'].play()

#         if playerVelY < playerMaxVelY and not playerFlapped:
#             playerVelY += playerAccY
#         if playerFlapped:
#             playerFlapped = False
#         playerHeight = GAME_SPRITES['player'].get_height()
#         playery += min(playerVelY, GROUNDY - playery - playerHeight)

#         for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
#             upperPipe['x'] += pipeVelX
#             lowerPipe['x'] += pipeVelX

#         if 0 < upperPipes[0]['x'] < 5:
#             newpipe = getRandomPipe()
#             upperPipes.append(newpipe[0])
#             lowerPipes.append(newpipe[1])

#         if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
#             upperPipes.pop(0)
#             lowerPipes.pop(0)

#         SCREEN.blit(GAME_SPRITES['background'], (0, 0))
#         for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
#             SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
#             SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
#         SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
#         SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

#         myDigits = [int(x) for x in list(str(score))]
#         width = sum([GAME_SPRITES['numbers'][digit].get_width() for digit in myDigits])
#         Xoffset = (SCREENWIDTH - width) / 2
#         for digit in myDigits:
#             SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
#             Xoffset += GAME_SPRITES['numbers'][digit].get_width()

#         pygame.display.update()
#         FPSCLOCK.tick(FPS)


# def isCollide(playerx, playery, upperPipes, lowerPipes):
#     if playery > GROUNDY - 25 or playery < 0:
#         GAME_SOUNDS['hit'].play()
#         return True

#     playerWidth = GAME_SPRITES['player'].get_width()
#     playerHeight = GAME_SPRITES['player'].get_height()

#     for pipe in upperPipes:
#         pipeHeight = GAME_SPRITES['pipe'][0].get_height()
#         if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
#             GAME_SOUNDS['hit'].play()
#             return True

#     for pipe in lowerPipes:
#         if playery + playerHeight > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
#             GAME_SOUNDS['hit'].play()
#             return True

#     return False


# def getRandomPipe():
#     pipeHeight = GAME_SPRITES['pipe'][0].get_height()
#     offset = SCREENHEIGHT / 3
#     y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
#     pipeX = SCREENWIDTH + 10
#     y1 = pipeHeight - y2 + offset
#     return [
#         {'x': pipeX, 'y': -y1},
#         {'x': pipeX, 'y': y2}
#     ]


# if __name__ == "__main__":
#     pygame.init()
#     FPSCLOCK = pygame.time.Clock()
#     pygame.display.set_caption('Flappy Bird by Waleed')

#     # Numbers
#     GAME_SPRITES['numbers'] = tuple(
#         pygame.transform.scale(
#             pygame.image.load(f'gallery/sprites/{i}.png').convert_alpha(),
#             (24, 36)
#         ) for i in range(10)
#     )

#     # Message
#     msg_img = pygame.image.load('gallery/sprites/message.png').convert_alpha()
#     GAME_SPRITES['message'] = pygame.transform.scale(msg_img, (200, 90))

#     # Base
#     base_img = pygame.image.load('gallery/sprites/base.png').convert_alpha()
#     GAME_SPRITES['base'] = pygame.transform.scale(base_img, (SCREENWIDTH, 100))

#     # Pipes
#     PIPE_WIDTH = 52
#     PIPE_HEIGHT = 320
#     pipe_img = pygame.image.load(PIPE).convert_alpha()
#     GAME_SPRITES['pipe'] = (
#         pygame.transform.scale(pygame.transform.rotate(pipe_img, 180), (PIPE_WIDTH, PIPE_HEIGHT)),
#         pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))
#     )

#     # Sounds
#     GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
#     GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
#     GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
#     GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
#     GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

#     # Background
#     bg_img = pygame.image.load(BACKGROUND).convert()
#     GAME_SPRITES['background'] = pygame.transform.scale(bg_img, (SCREENWIDTH, SCREENHEIGHT))

#     # Bird
#     bird_img = pygame.image.load(PLAYER).convert_alpha()
#     w, h = bird_img.get_size()
#     BIRD_SCALE = 0.15
#     bird_img = pygame.transform.scale(bird_img, (int(w * BIRD_SCALE), int(h * BIRD_SCALE)))
#     GAME_SPRITES['player'] = bird_img

#     while True:
#         welcomeScreen()
#         mainGame()



import random
import sys
import pygame
from pygame.locals import *


FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/bg.png'  
PIPE = 'gallery/sprites/pillar.png'     
BIRD_SCALE = 0.12 

def welcomeScreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerAccY = 1
    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        if isCollide(playerx, playery, upperPipes, lowerPipes):
            GAME_SOUNDS['die'].play()
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery += min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = sum([GAME_SPRITES['numbers'][digit].get_width() for digit in myDigits])
        Xoffset = (SCREENWIDTH - width) / 2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    
   
    player_w = GAME_SPRITES['player'].get_width()
    player_h = GAME_SPRITES['player'].get_height()
    playerRect = pygame.Rect(playerx, playery, player_w, player_h)

    
    pipe_w = GAME_SPRITES['pipe'][0].get_width()
    pipe_h = GAME_SPRITES['pipe'][0].get_height()

    for pipe in upperPipes:
      
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], pipe_w, pipe_h)
        if playerRect.colliderect(pipeRect):
            GAME_SOUNDS['hit'].play()
            return True

 
    for pipe in lowerPipes:
        
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], pipe_w, pipe_h)
        if playerRect.colliderect(pipeRect):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    return [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Waleed')

    
    GAME_SPRITES['numbers'] = tuple(
        pygame.transform.scale(
            pygame.image.load(f'gallery/sprites/{i}.png').convert_alpha(),
            (24, 36)
        ) for i in range(10)
    )

    
    msg_img = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['message'] = pygame.transform.scale(msg_img, (200, 90))

    
    base_img = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.transform.scale(base_img, (SCREENWIDTH, 100))

    
    PIPE_WIDTH = 52
    PIPE_HEIGHT = 320
    pipe_img = pygame.image.load(PIPE).convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.scale(pygame.transform.rotate(pipe_img, 180), (PIPE_WIDTH, PIPE_HEIGHT)),
        pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))
    )

    
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    
    bg_img = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['background'] = pygame.transform.scale(bg_img, (SCREENWIDTH, SCREENHEIGHT))

    bird_img = pygame.image.load(PLAYER).convert_alpha()
    w, h = bird_img.get_size()
    BIRD_SCALE = 0.15
    bird_img = pygame.transform.scale(bird_img, (int(w * BIRD_SCALE), int(h * BIRD_SCALE)))
    GAME_SPRITES['player'] = bird_img

    while True:
        welcomeScreen()
        mainGame()
