import pygame
import random 
import sys
from pygame.locals import *

#setttings
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=510
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8 #matlab height ka 80 perc ground
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER="Gallery/Sprites/bird.png"
BACKGROUND="Gallery/Sprites/bg.png"
PIPE="Gallery/Sprites/pillar.png"
BIRD_SCALE = 0.12  # 0.1 = very small, 0.5 = bigger, 1 = original size

BASE="Gallery/Sprites/base.png"
# MESSAGE="Gallery/Sprites/message.png"

def welcomescreen():
    """
     yeh welcome images screen p dikhayga
    """
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES["player"].get_height())/2)
    # messagex=int((SCREENWIDTH-GAME_SPRITES["message"].get_width())/2)
    # messagey=int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            #if cross or exit clicked
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key==pygame.K_UP):
                return 
            else: 
                SCREEN.blit(GAME_SPRITES["background"],(0,0))
                SCREEN.blit(GAME_SPRITES["player"],(playerx,playery))
                # SCREEN.blit(GAME_SPRITES["message"],(messagex,messagey))
                # SCREEN.blit(GAME_SPRITES["base"],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT/2)
    basex=0
    # creating pipes
    newpipe1 = getrandompipe()
    newpipe2 = getrandompipe()
          
    # CORRECTION: ensure [0] is used for upper and [1] for lower consistently
    upperpipes = [
        {"x": SCREENWIDTH + 200, "y": newpipe1[0]["y"]},
        {"x": SCREENWIDTH + 200 + (SCREENWIDTH / 2), "y": newpipe2[0]["y"]}, # You had newpipe2[1] here
    ]
    lowerpipes = [
        {"x": SCREENWIDTH + 200, "y": newpipe1[1]["y"]}, # You had newpipe1[0] here
        {"x": SCREENWIDTH + 200 + (SCREENWIDTH / 2), "y": newpipe2[1]["y"]}, 
    ]
          
    pipevelx=-4
    playervely=-9
    playermaxvely=10
    playerminvely=-8
    playeraccy=1
    
    playerFlapv=-8
    playerFlapped=False
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.QUIT()
                sys.exit()
            if event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key==pygame.K_UP):
                if playery>0:
                    playervely = playerFlapv
                    playerFlapped=True
                    GAME_SOUNDS["wing"].play()
                     
    
        crashtest=iscollide(playerx,playery,upperpipes,lowerpipes)
        if crashtest:
            return
                    
        #checking score
        playermidpos=playerx+GAME_SPRITES["player"].get_width()/2
        for pipe in upperpipes:
            pipemidpos=pipe["x"]+GAME_SPRITES["pipe"][0].get_width()/2
            if pipemidpos<= playermidpos<pipemidpos+4:
                score+=1
                GAME_SOUNDS["point"].play()
                print(f"your score is{score}")
            
            
        if playervely<playermaxvely and not playerFlapped:
            playervely+=playeraccy
        if playerFlapped:
            playerFlapped=False
        playerheight=GAME_SPRITES["player"].get_height()
        playery=playery+min(playervely,GROUNDY-playery-playerheight)
        
        #making pipes move
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):  #zip joins two lists in oredered pair
           upperpipe["x"]+=pipevelx
           lowerpipe["x"]+=pipevelx
           
        #adding new pipes
        if 0<upperpipes[0]["x"]<5:
            newpipe=getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
            
        #extra pipe ko remove kryngy
        if upperpipes[0]["x"] < -GAME_SPRITES["pipe"][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
            
        #drawing sprites on screen by blitting
        SCREEN.blit(GAME_SPRITES["background"],(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes): 
               SCREEN.blit(GAME_SPRITES["pipe"][0], (upperpipe["x"], upperpipe["y"]))
               SCREEN.blit(GAME_SPRITES["pipe"][1], (lowerpipe["x"], lowerpipe["y"]))
        # SCREEN.blit(GAME_SPRITES["base"],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES["player"],(playerx,playery))
        mydigits=[int(x) for x in list(str(score))]
        width=0
        for digit in mydigits:
            width +=GAME_SPRITES["numbers"][digit].get_width()
        xoffset=(SCREENWIDTH-width)/2
        
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES["numbers"][digit],(xoffset,SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES["numbers"][digit].get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
            

            
        
        
            
            
            
def iscollide(playerx, playery, upperpipes, lowerpipes):
    # 1. Create a Rectangle for the Bird
    # pygame.Rect(x, y, width, height)
    bird_w = GAME_SPRITES["player"].get_width()
    bird_h = GAME_SPRITES["player"].get_height()
    playerRect = pygame.Rect(playerx, playery, bird_w, bird_h)

    # 2. Check if bird hit the Ground or Ceiling
    # If the BOTTOM of the bird hits the ground (GROUNDY)
    if playery + bird_h >= GROUNDY - 1 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    # 3. Check collision with Upper Pipes
    pipe_w = GAME_SPRITES["pipe"][0].get_width()
    pipe_h = GAME_SPRITES["pipe"][0].get_height()

    for pipe in upperpipes:
        # Create a box for the pipe
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], pipe_w, pipe_h)
        # Ask pygame if they are touching
        if playerRect.colliderect(pipeRect):
            GAME_SOUNDS['hit'].play()
            return True

    # 4. Check collision with Lower Pipes
    for pipe in lowerpipes:
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], pipe_w, pipe_h)
        if playerRect.colliderect(pipeRect):
            GAME_SOUNDS['hit'].play()
            return True

    return False
  
def getrandompipe():
    pipeheight = GAME_SPRITES["pipe"][0].get_height()
    offset = SCREENHEIGHT / 3
    max_y = SCREENHEIGHT - GAME_SPRITES["base"].get_height() - 1.2*offset
    if max_y < 0:
        max_y = 0
    y2 = offset + random.randrange(0, int(max_y + 1))  # +1 to avoid empty range
    pipex = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {"x": pipex, "y": -y1},
        {"x": pipex, "y": y2}
    ]
    return pipe


if __name__ == '__main__':
#starting game
    pygame.init() #initialze pygame moudles
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Waleed")
    GAME_SPRITES["numbers"]=(
        pygame.image.load("Gallery/Sprites/0.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/1.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/2.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/3.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/4.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/5.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/6.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/7.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/8.png").convert_alpha(),
        pygame.image.load("Gallery/Sprites/9.png").convert_alpha()
)
    GAME_SPRITES["base"]=pygame.image.load("Gallery/Sprites/base.png").convert_alpha()

    GAME_SPRITES["pipe"]=(
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    # GAME_SPRITES["message"]=pygame.image.load(MESSAGE).convert_alpha()
    GAME_SPRITES["background"]=pygame.image.load(BACKGROUND).convert_alpha()
    bird_img = pygame.image.load(PLAYER).convert_alpha()
    w, h = bird_img.get_size()
    bird_img = pygame.transform.scale(bird_img, (int(w * BIRD_SCALE), int(h * BIRD_SCALE)))
    GAME_SPRITES["player"] = bird_img


    #making sounds
    GAME_SOUNDS["die"]=pygame.mixer.Sound("Gallery/audio/die.wav")
    GAME_SOUNDS["swoosh"]=pygame.mixer.Sound("Gallery/audio/swoosh.wav")
    GAME_SOUNDS["hit"]=pygame.mixer.Sound("Gallery/audio/hit.wav")
    GAME_SOUNDS["wing"]=pygame.mixer.Sound("Gallery/audio/wing.wav")
    GAME_SOUNDS["point"]=pygame.mixer.Sound("Gallery/audio/point.wav")


    while True:
     welcomescreen()
     maingame()
