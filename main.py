import pygame
from random import randint, choice
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player1 = pygame.image.load('textures/player1.png')
        player2 = pygame.image.load('textures/player_walk_2.png')
        self.playerCrouch = pygame.image.load('textures/crouch.png')
        self.playerJump = pygame.image.load('textures/jump.png')
        self.playerWalk = [player1, player2]
        self.playerIndex = 0

        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.gravity = 0

        self.jumpSound = pygame.mixer.Sound('audio/jump.mp3')

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20



    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom < 300:
            self.image = self.playerJump
        #elif keys[pygame.K_DOWN]:
            #self.image = self.playerCrouch
            #self.rect.y = 2
        else:
            self.playerIndex += 0.1
            if self.playerIndex >= len(self.playerWalk):
                self.playerIndex = 0
            self.image = self.playerWalk[int(self.playerIndex)]

    def update(self):
        self.playerInput()
        self.animation()
        self.applyGravity()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly1 = pygame.image.load('textures/Fly1.png').convert_alpha()
            fly2 = pygame.image.load('textures/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            yPos = 250

        else:
            snail1 = pygame.image.load('textures/meteor.png').convert_alpha()
            snail2 = pygame.image.load('textures/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            yPos = 300

        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom=(900, yPos))

    def animationState(self):
        self.animationIndex += 0.1
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def update(self):
        self.animationState()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def collisionSprite():
    if pygame.sprite.spritecollide(play.sprite, obstacle, False):
        obstacle.empty()
        return False
    else:
        return True
def scoreDisplay():
    time = int(pygame.time.get_ticks()/1000) - startTime
    score = font.render(f'Score: {time}', False, "blue")
    scoreRect= score.get_rect(center=(400, 85))
    screen.blit(score, scoreRect)
    return time

def obstacleMovement(obstacleList):
    if obstacleList:
        for obstacleRect in obstacleList:
            obstacleRect.x -= 5

            if obstacleRect.bottom == 300:
                screen.blit(meteor, obstacleRect)
            else:
                screen.blit(fly, obstacleRect)

        obstacleList = [obstacle for obstacle in obstacleList if obstacle.x > -100]

        return obstacleList
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacleRect in obstacles:
            if player.colliderect(obstacleRect):
                return False
    return True


def playerAnimation ():
    global player, playerIndex

    # play jump when player not on floor
    if playerRect.bottom < 300:
        player = playerJump
    else:  # play walk animation when on floor
        playerIndex += 0.1
        if playerIndex >= len(playerWalk):
            playerIndex = 0
        player = playerWalk[int(playerIndex)]


pygame.init()

# Game Variable
gameActive = False
startTime = 0
score = 0

play = pygame.sprite.GroupSingle()
play.add(Player())

obstacle = pygame.sprite.Group()
# Create screen and name it
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Galaxy Runner")

# text
font = pygame.font.Font('text/Pixeltype.ttf', 50)
title = pygame.font.Font('text/Pixeltype.ttf', 100)


# surfaces
sky = pygame.image.load('textures/sky.png').convert_alpha()
ground = pygame.image.load('textures/ground.png').convert_alpha()
background = pygame.image.load("textures/stars.png").convert_alpha()

text = font.render("Galaxy Runner", False, "blue")
textRect = text.get_rect(center = (400, 50))


# Set frame rates
clock = pygame.time.Clock()

# Snail
snail1 = pygame.image.load('textures/meteor.png').convert_alpha()
snail2 = pygame.image.load('textures/snail2.png').convert_alpha()
snailStand = pygame.image.load('textures/meteor.png').convert_alpha()
snailStand = pygame.transform.rotozoom(snailStand, 0, 1.5)
snailStandRect = snailStand.get_rect(center=(70, 75))
snailFrames = [snail1, snail2]
snailIndex = 0
meteor = snailFrames[snailIndex]

# Fly
fly1 = pygame.image.load('textures/Fly1.png').convert_alpha()
fly2 = pygame.image.load('textures/Fly2.png').convert_alpha()
flyFrames = [fly1, fly2]
flyIndex = 0
fly = flyFrames[flyIndex]

obstacleRectList = []

player1 = pygame.image.load('textures/player1.png').convert_alpha()
player2 = pygame.image.load('textures/player_walk_2.png').convert_alpha()
playerJump = pygame.image.load('textures/jump.png').convert_alpha()
playerWalk = [player1, player2]
playerIndex = 0

player = playerWalk[playerIndex]

playerRect = player.get_rect(midbottom=(80, 300))
playerGravity = 0

# Intro Screen
playerStand = pygame.image.load('textures/player_stand.png').convert_alpha()
playerStand = pygame.transform.rotozoom(playerStand, 0, 1.5)
playerStandRect = playerStand.get_rect(center=(730, 50))

# Timer
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1200)

snailTimer = pygame.USEREVENT + 2
pygame.time.set_timer(snailTimer, 300)

flyTimer = pygame.USEREVENT + 3
pygame.time.set_timer(flyTimer, 100)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameActive:
            if event.type == obstacleTimer:
                obstacle.add(Obstacles(choice(['fly', 'snail','snail','snail'])))


    if gameActive:

        screen.blit(sky,(0,0))
        screen.blit(ground,(0, 300))


        # Player
        play.draw(screen)
        play.update()

        # Enemy movement
        obstacle.draw(screen)
        obstacle.update()

        screen.blit(text, textRect)
        score = scoreDisplay()

        # Collision
        gameActive = collisionSprite()

    elif gameActive == False:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            gameActive = True
            startTime = int(pygame.time.get_ticks() / 1000)
        obstacleRectList.clear()
        playerRect.midbottom = (80, 300)
        playerGravity = 0

        scoreText = font.render(f'Your Score: {score}', False, "white")
        scoreTextRect = scoreText.get_rect(center=(400, 330))

        titleText = title.render("Galaxy Runner", False, "white")
        titleTextRect = titleText.get_rect(center=(400, 100))

        playText = font.render("Press Space To Play", False, "white")
        playerTextRect = playText.get_rect(center=(400, 200))
        pygame.draw.rect(screen, (0,0,0), playerTextRect)
        playerStandRect = playerStand.get_rect(center=(730, 75))

        howText = font.render("How To Play", False, 'white')
        howRect = howText.get_rect(center= (400,265))

        snailStandRect = snailStand.get_rect(center=(70, 100))

        screen.blit(background, (0,0))
        screen.blit(snailStand, snailStandRect)
        screen.blit(playerStand, playerStandRect)
        screen.blit(howText, howRect)
        screen.blit(titleText, titleTextRect)
        screen.blit(playText, playerTextRect)
        if score > 0:
            screen.blit(scoreText, scoreTextRect)

    pygame.display.update()
    clock.tick(60)
