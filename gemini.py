import pygame
import random
import sys
from pygame.locals import *

# ==============================
# Game Settings
# ==============================
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Flappy Bird by Waleed")

BIRD_SCALE = 0.12
PIPE_SCALE = 0.25  # adjust to fill screen nicely
PIPE_GAP = 100     # vertical gap between pipes

# ==============================
# Sprites and Sounds
# ==============================
GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = "Gallery/Sprites/bird.png"
BACKGROUND = "Gallery/Sprites/bg.png"
PIPE = "Gallery/Sprites/pillar.png"
BASE = "Gallery/Sprites/base.png"

# ==============================
# Welcome Screen
# ==============================
def welcomescreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height()) / 2)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
        SCREEN.blit(GAME_SPRITES["background"], (0,0))
        SCREEN.blit(GAME_SPRITES["player"], (playerx, playery))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# ==============================
# Main Game Loop
# ==============================
def maingame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    playerVelY = 0
    playerAccY = 1
    playerMaxVelY = 10
    playerFlapVel = -9
    playerFlapped = False

    pipeVelX = -4

    # Initial pipes
    upperpipes = []
    lowerpipes = []
    for i in range(2):
        newpipe = getrandompipe()
        upperpipes.append(newpipe[0])
        lowerpipes.append(newpipe[1])

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                playerVelY = playerFlapVel
                playerFlapped = True
                GAME_SOUNDS["wing"].play()

        # Collision
        if iscollide(playerx, playery, upperpipes, lowerpipes):
            GAME_SOUNDS["die"].play()
            return

        # Score
        playerMidPos = playerx + GAME_SPRITES["player"].get_width() / 2
        for pipe in upperpipes:
            pipeMidPos = pipe["x"] + GAME_SPRITES["pipe"][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                GAME_SOUNDS["point"].play()

        # Player movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playery += min(playerVelY, GROUNDY - playery - GAME_SPRITES["player"].get_height())

        # Move pipes
        for uPipe, lPipe in zip(upperpipes, lowerpipes):
            uPipe["x"] += pipeVelX
            lPipe["x"] += pipeVelX

        # Add new pipe
        if upperpipes[0]["x"] < SCREENWIDTH - 150:
            newpipe = getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        # Remove offscreen pipe
        if upperpipes[0]["x"] < -GAME_SPRITES["pipe"][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # Draw everything
        SCREEN.blit(GAME_SPRITES["background"], (0,0))
        for uPipe, lPipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES["pipe"][0], (uPipe["x"], uPipe["y"]))
            SCREEN.blit(GAME_SPRITES["pipe"][1], (lPipe["x"], lPipe["y"]))
        SCREEN.blit(GAME_SPRITES["player"], (playerx, playery))

        # Draw score
        mydigits = [int(x) for x in str(score)]
        width = sum(GAME_SPRITES["numbers"][digit].get_width() for digit in mydigits)
        Xoffset = (SCREENWIDTH - width) / 2
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES["numbers"][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES["numbers"][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# ==============================
# Collision detection
# ==============================
def iscollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - GAME_SPRITES["player"].get_height() or playery < 0:
        GAME_SOUNDS["hit"].play()
        return True
    playerRect = GAME_SPRITES["player"].get_rect(topleft=(playerx, playery))
    for uPipe, lPipe in zip(upperpipes, lowerpipes):
        uRect = GAME_SPRITES["pipe"][0].get_rect(topleft=(uPipe["x"], uPipe["y"]))
        lRect = GAME_SPRITES["pipe"][1].get_rect(topleft=(lPipe["x"], lPipe["y"]))
        if playerRect.colliderect(uRect) or playerRect.colliderect(lRect):
            GAME_SOUNDS["hit"].play()
            return True
    return False

# ==============================
# Generate random pipes
# ==============================
def getrandompipe():
    """
    Generate positions for upper and lower pipes with a proper gap
    """
    pipeHeight = GAME_SPRITES["pipe"][0].get_height()
    gapY = random.randrange(int(SCREENHEIGHT*0.2), int(SCREENHEIGHT*0.6))
    pipeX = SCREENWIDTH + 10

    upperPipeY = gapY - pipeHeight
    lowerPipeY = gapY + PIPE_GAP

    return [
        {"x": pipeX, "y": upperPipeY},  # upper pipe
        {"x": pipeX, "y": lowerPipeY}   # lower pipe
    ]


# ==============================
# Main Program
# ==============================
if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # Load numbers
    GAME_SPRITES["numbers"] = tuple(pygame.image.load(f"Gallery/Sprites/{i}.png").convert_alpha() for i in range(10))

    # Load base
    GAME_SPRITES["base"] = pygame.image.load(BASE).convert_alpha()

    # Load and scale pillars
    pipe_img = pygame.image.load(PIPE).convert_alpha()
    w, h = pipe_img.get_size()
    pipe_img = pygame.transform.scale(pipe_img, (int(w * PIPE_SCALE), int(h * PIPE_SCALE)))
    GAME_SPRITES["pipe"] = (pygame.transform.rotate(pipe_img, 180), pipe_img)

    # Background
    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert_alpha()

    # Bird
    bird_img = pygame.image.load(PLAYER).convert_alpha()
    w, h = bird_img.get_size()
    bird_img = pygame.transform.scale(bird_img, (int(w * BIRD_SCALE), int(h * BIRD_SCALE)))
    GAME_SPRITES["player"] = bird_img

    # Sounds
    GAME_SOUNDS["die"] = pygame.mixer.Sound("Gallery/audio/die.wav")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("Gallery/audio/swoosh.wav")
    GAME_SOUNDS["hit"] = pygame.mixer.Sound("Gallery/audio/hit.wav")
    GAME_SOUNDS["wing"] = pygame.mixer.Sound("Gallery/audio/wing.wav")
    GAME_SOUNDS["point"] = pygame.mixer.Sound("Gallery/audio/point.wav")

    while True:
        welcomescreen()
        maingame()
