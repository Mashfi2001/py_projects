import pygame, asyncio
#to randomize enemy position
import random
#for distence
import math
#for music
from pygame import mixer


#intialize the pygame
pygame.init()

#create the screen(width, hight)
screen = pygame.display.set_mode((800, 600))

#Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Background
background = pygame.image.load('brick background.png')

#Background music
mixer.music.load('background2.wav')
mixer.music.play(-1)

#enemy(updated to get multiple enemy)
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load('aircraft.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.07)
    enemyy_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

#player
playerimg = pygame.image.load('spaceship.png')
playerx = 370
playery = 480
playerx_change = 0


#newupdated
def player(x, y):
    screen.blit(playerimg, (x, y))

#Bullet extra: Ready - You can't see the bullet on the screen
#              Fire - bullet is currently moving
bulletimg = pygame.image.load('bullet.png')
bulletx = 370
bullety = 480
bulletx_change = 0
bullety_change = 0.4
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))

#collision
def isCollision(enemyx, enemyy, bulletx, bullety):
    distence = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distence < 30:
        return True
    else:
        return False
    
#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',16)

textx = 10
texty = 10

def show_score(x, y):
    score = font.render(f"Score: {str(score_value)}", True, (0, 0, 0))
    screen.blit(score, (x ,y))

#Game over text
game_ov = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    ov = game_ov.render('GAME OVER', True, (0, 0 ,0))
    screen.blit(ov, (200, 250))

    
#Game loop(infinite loop to keep the game running)
running = True
while running:

    #RGB - Red, Green, Blue = background
    screen.fill((255,255,255))

    #Backgound image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #if keystoke is pressed check whether its right or left
        #if you put playerx -+= any in here this will create some thing like precise movement or not holding the type of thing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.1
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.1
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # Get the current coordinate of the spaceship
                    bulletx = playerx
                    fire_bullet(bulletx, bullety) #if we use playerx here the bullet will change its coordinate with the spaceship
                    
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        #if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    
    #calculation
    playerx += playerx_change

    #boundaries
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

 
    #enemy movements or boundaries

    for i in range(num_of_enemy):
        #Game over
        if enemyy[i] > 440:
            for j in range(num_of_enemy):
                enemyy[j] = 2000
            game_over_text()
            break

        #enemy calculation
        enemyx[i] += enemyx_change[i]   
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.07
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.07
            enemyy[i] += enemyy_change[i]
        #collision
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision is True:
            #bullet collision
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            bullety = 480
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0, 800)
            enemyy[i] = random.randint(50, 150)

        #for enemy to apper
        enemy(enemyx[i], enemyy[i], i)


    #Bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change
  

    #for player to apper
    player(playerx, playery)

    #show score
    show_score(textx, texty)

    #update
    pygame.display.update()