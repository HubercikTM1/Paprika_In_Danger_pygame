import pygame as pg
import random as rnd
import math
from pygame import mixer

pg.init()

screen = pg.display.set_mode((1000,800))

bg = pg.image.load("background.png")

#bg music
mixer.music.load('bgmusic.wav')
mixer.music.play(-1)

title = pg.display.set_caption("Paprika In Danger")
icon = pg.image.load("paprika.png")
pg.display.set_icon(icon)

#PLAYER
playerImg = pg.image.load("hamster.png")
playerX = 460
playerY = 700
playerX_changed = 0

#ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_changed = []
enemyY_changed = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pg.image.load("paprika_enemy.png"))
    enemyX.append(rnd.randint(0,935))
    enemyY.append(rnd.randint(50,150))
    enemyX_changed.append(0.3)
    enemyY_changed.append(40)

#BULLET
bulletImg = pg.image.load("bullet.png")
bulletX = 0
bulletY = 700
bulletY_changed = 1
#ready - you can't see the bullet on the screen
#fire - the bullet is currently moving
bullet_state = "ready"

#score
score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over
game_over_font = pg.font.Font('freesansbold.ttf', 100)

def game_over():
    game_over_text = game_over_font.render('GAME OVER', True, (255,255,255))
    screen.blit(game_over_text, (200,350))


def show_score(x,y):
    score = font.render("Score: "+ str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    #blit = draw
    screen.blit(playerImg, (x, y))

def enemy(x,y, i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10))

#distance betweenm two points and the midpoint:
    # D = pierwiastek z (x2 - x1)2 + (y2 - y1)2
def isCoolision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if(distance < 27):
        return True
    else:
        return False


isRunning = True
while isRunning:

    screen.fill((0, 0, 0))

    screen.blit(bg, (0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_changed = -0.5
            if event.key == pg.K_RIGHT:
                playerX_changed = 0.5
            if event.key == pg.K_SPACE:
                if(bullet_state == "ready"):
                    bullet_sound = mixer.Sound('shot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_changed = 0


    #player movement
    playerX += playerX_changed
    if(playerX <= 0):
        playerX=0
    elif(playerX >= 936):
        playerX=936

    #enemy movement
    for i in range(num_of_enemies):

        #game over
        if(enemyY[i] > 640):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_changed[i]
        if(enemyX[i] <= 0):
            enemyX_changed[i] = 0.3
            enemyY[i] += enemyY_changed[i]
        elif(enemyX[i] >= 936):
            enemyX_changed[i] = -0.3
            enemyY[i] += enemyY_changed[i]

        # Collision
        collision = isCoolision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_kill = mixer.Sound('kill.wav')
            bullet_kill.play()
            bulletY = 700
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = rnd.randint(0, 935)
            enemyY[i] = rnd.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if(bulletY <= 0):
        bulletY = 700
        bullet_state = "ready"

    if(bullet_state == "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_changed


    player(playerX, playerY)
    show_score(textX, textY)

    pg.display.update()
