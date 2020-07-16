import pygame
import math

import random
from pygame import mixer

pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))
# Backround
Backround = pygame.image.load('backround1.png')
# Backround sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("SpaceWars")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# PlayerOne
player1 = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# MoreEnemy
Enemyimg = []
EnemyX = []
EnemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemys = 6

# EnemyPlayer
for i in range(num_of_enemys):
    Enemyimg.append(pygame.image.load('outer-space.png'))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(15, 35))
    enemyX_change.append(3)
    enemyY_change.append(30)

# bullet
# Ready - you cant see the bullet on the screen
# Fire - the bullet moving
bulletimg = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('SPACE.ttf', 16)
textX = 10
textY = 10

# GameOver text
text_over = pygame.font.Font('SPACE.ttf', 64)
Effect = pygame.mixer.Sound('Gameover.wav')


def game_over():
    font = text_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(font, (130, 250))


def show_score(x, y):
    score = font.render("Score:\n" + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player1, (x, y))


def Enemy(x, y, i):
    screen.blit(Enemyimg[i], (x, y,))


def Fire_Bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(EnemyX, EnemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(EnemyX - bulletX, 2)) + (math.pow(EnemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(Backround, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_UP:
                playerY_change = -4
            if event.key == pygame.K_DOWN:
                playerY_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    Fire_Bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # cheking for boundaries
    playerY += playerY_change
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # enemy movement
    for i in range(num_of_enemys):

        # Game over
        if EnemyY[i] > 90:

            for j in range(num_of_enemys):
                EnemyY[j] = 2000
            
            Effect.play()
            game_over()

            break

        EnemyX[i] += enemyX_change[i]
        if EnemyX[i] <= 0:
            enemyX_change[i] = 3
            EnemyY[i] += enemyY_change[i]

        elif EnemyX[i] >= 736:
            enemyX_change[i] = -3
            EnemyY[i] += enemyY_change[i]

        # COLLISION
        collision = iscollision(EnemyX[i], EnemyY[i], bulletX, bulletY)

        if collision:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 650
            bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)

        Enemy(EnemyX[i], EnemyY[i], i)

    # Bullet movement:
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "Fire":
        Fire_Bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
