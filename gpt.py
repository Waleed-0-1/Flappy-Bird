import pygame
import random
import sys
from pygame.locals import *

# --- GLOBAL SETTINGS ---
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GAME_SPRITES = {}
GAME_SOUNDS = {}

# --- ASSETS ---
PLAYER_IMG = 'bird.png'
BACKGROUND_IMG = 'bg.png'
PIPE_IMG = 'pillar.png'
NUMBERS = [f'{i}.png' for i in range(10)]

AUDIO_FILES = {
    'die': 'die.wav',
    'hit': 'hit.wav',
    'point': 'point.wav',
    'swoosh': 'swoosh.wav',
    'wing': 'wing.wav'
}

# --- SCALE FACTORS ---
BIRD_SCALE = 0.12
PIPE_SCALE = 0.3
NUMBER_SCALE = 0.2

# --- FUNCTIONS ---
def load_assets():
    # Load numbers
    numbers_imgs = []
    for file in NUMBERS:
        img = pygame.image.load(f'Gallery/Sprites/{file}').convert_alpha()
        w,h = img.get_size()
        img = pygame.transform.scale(img, (int(w*NUMBER_SCALE), int(h*NUMBER_SCALE)))
        numbers_imgs.append(img)
    GAME_SPRITES['numbers'] = numbers_imgs

    # Load bird
    bird_img = pygame.image.load(f'Gallery/Sprites/{PLAYER_IMG}').convert_alpha()
    w,h = bird_img.get_size()
    bird_img = pygame.transform.scale(bird_img, (int(w*BIRD_SCALE), int(h*BIRD_SCALE)))
    GAME_SPRITES['player'] = bird_img

    # Load pipes
    pipe_img = pygame.image.load(f'Gallery/Sprites/{PIPE_IMG}').convert_alpha()
    w,h = pipe_img.get_size()
    pipe_img = pygame.transform.scale(pipe_img, (int(w*PIPE_SCALE), int(h*PIPE_SCALE)))
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pipe_img, 180), pipe_img)  # upper, lower

    # Load background
    GAME_SPRITES['background'] = pygame.image.load(f'Gallery/Sprites/{BACKGROUND_IMG}').convert()

    # Base
    base_surf = pygame.Surface((SCREENWIDTH, int(SCREENHEIGHT*0.2)))
    base_surf.fill((222,184,135))
    pygame.draw.line(base_surf, (34,139,34), (0,0), (SCREENWIDTH,0), 10)
    GAME_SPRITES['base'] = base_surf

    # Load sounds
    for key, file in AUDIO_FILES.items():
        GAME_SOUNDS[key] = pygame.mixer.Sound(f'Gallery/audio/{file}')

def welcome_screen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((GROUNDY - GAME_SPRITES['player'].get_height()) / 2)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return

        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def get_random_pipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    max_y = SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset
    if max_y < 0:
        max_y = 0
    y2 = offset + random.randrange(0, int(max_y + 1))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    return [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]

def is_collide(playerx, playery, upperpipes, lowerpipes):
    playerW = GAME_SPRITES['player'].get_width()
    playerH = GAME_SPRITES['player'].get_height()

    # Ground or ceiling
    if playery > GROUNDY - 5 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    # Pipes
    for pipe in upperpipes:
        if (playerx + playerW > pipe['x'] and playerx < pipe['x'] + GAME_SPRITES['pipe'][0].get_width()) and (playery < pipe['y'] + GAME_SPRITES['pipe'][0].get_height()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playerx + playerW > pipe['x'] and playerx < pipe['x'] + GAME_SPRITES['pipe'][1].get_width()) and (playery + playerH > pipe['y']):
            GAME_SOUNDS['hit'].play()
            return True

    return False

def main_game():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int((GROUNDY - GAME_SPRITES['player'].get_height()) / 2)
    basex = 0

    newPipe1 = get_random_pipe()
    newPipe2 = get_random_pipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']}
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerAccY = 1
    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        if is_collide(playerx, playery, upperPipes, lowerPipes):
            return

        # Score update
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                GAME_SOUNDS['point'].play()

        # Player movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playery += min(playerVelY, GROUNDY - playery - GAME_SPRITES['player'].get_height())

        # Move pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add new pipe
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = get_random_pipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # Remove passed pipe
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Draw everything
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        # Draw score
        myDigits = [int(x) for x in str(score)]
        width = sum(GAME_SPRITES['numbers'][digit].get_width() for digit in myDigits)
        Xoffset = (SCREENWIDTH - width) // 2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.05))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# --- MAIN ---
if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Chiggaa")
    load_assets()
    while True:
        welcome_screen()
        main_game()
