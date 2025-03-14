import pygame
import sys
import random
from math import *

pygame.init()

width = 500
height = 500
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("DODGE THE TUYOM")
clock = pygame.time.Clock()

background = (255, 255, 255)
playerColor = (200, 200, 100)

red = (203, 67, 53)
yellow = (241, 196, 15)
blue = (46, 134, 193)
green = (34, 153, 84)
purple = (136, 78, 160)
orange = (214, 137, 16)

colors = [red, yellow, blue, green, purple, orange]

score = 0
high_score = 0  # Variable to keep track of high score

# Function to load high score from a file
def load_high_score():
    global high_score
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0  # Set high score to 0 if the file doesn't exist

# Function to save the high score to a file
def save_high_score():
    global high_score
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

class SeaUrchin:
    def __init__(self, radius, speed):
        self.x = 0
        self.y = 0
        self.r = radius
        self.color = 0
        self.speed = speed
        self.angle = 0
    
    def createSeaUrchin(self):
        self.x = width / 2 - self.r
        self.y = height / 2 - self.r
        self.color = random.choice(colors)
        self.angle = random.randint(-180, 180)
    
    def move(self):
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        if self.x < self.r or self.x + self.r > width:
            self.angle = 180 - self.angle
        if self.y < self.r or self.y + self.r > height:
            self.angle *= -1

    def draw(self):
        pygame.draw.circle(display, self.color, (int(self.x), int(self.y)), self.r)

        # Draw spikes
        num_spikes = 12  # Number of spikes
        for i in range(num_spikes):
            angle = radians(i * (360 / num_spikes))
            x1 = self.x + self.r * cos(angle)
            y1 = self.y + self.r * sin(angle)
            x2 = self.x + (self.r + 8) * cos(angle)  # Outer spike end
            y2 = self.y + (self.r + 8) * sin(angle)
            pygame.draw.line(display, self.color, (x1, y1), (x2, y2), 2)


    def collision(self, radius):
        pos = pygame.mouse.get_pos()

        dist = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5

        if dist <= self.r + radius:
            gameOver()

class Target:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = self.w

    def generateNewCoord(self):
        self.x = random.randint(self.w, width - self.w)
        self.y = random.randint(self.h, height - self.h)

    def draw(self):
        color = random.choice(colors)
        pygame.draw.rect(display, color, (self.x, self.y, self.w, self.h))

    
def gameOver():
    global high_score  # Make sure to update the global high score
    loop = True
    font = pygame.font.SysFont("Agency FB", 100)
    text = font.render("Game Over!", True, (0, 0, 0))
    
    global score
    if score > high_score:  # Update high score if necessary
        high_score = score
        save_high_score()  # Save the new high score

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()

        display.fill(background)
        display.blit(text, (20, height / 2 - 100))
        displayScore()
        pygame.display.update()
        clock.tick()

def checkCollision(target, d, objTarget):
    pos = pygame.mouse.get_pos()
    dist = ((pos[0] - target[0] - objTarget.w) ** 2 + (pos[1] - target[1] - objTarget.h) ** 2) ** 0.5

    if dist <= d + objTarget.w:
        return True
    return False


def drawPlayerPointer(pos, r):
    pygame.draw.ellipse(display, playerColor, (pos[0] - r, pos[1] - r, 2 * r, 2 * r))


def close():
    pygame.quit()
    sys.exit()


def displayScore():
    font = pygame.font.SysFont("Arial", 30)
    scoreText = font.render(f"Score: {score}                                Best Score: {high_score}", True, (0, 0, 100))
    display.blit(scoreText, (10, 10))

def gameLoop():
    global score
    score = 0
    
    loop = True

    pRadius = 10

    balls = []

    for i in range(1):
        newBall = SeaUrchin(pRadius + 2, 5)
        newBall.createSeaUrchin()
        balls.append(newBall)

    target = Target()
    target.generateNewCoord()
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()

        display.fill(background)

        for i in range(len(balls)):
            balls[i].move()
            
        for i in range(len(balls)):
            balls[i].draw()
            
        for i in range(len(balls)):
            balls[i].collision(pRadius)

        playerPos = pygame.mouse.get_pos()
        drawPlayerPointer((playerPos[0], playerPos[1]), pRadius)

        collide = checkCollision((target.x, target.y), pRadius, target)
        
        if collide:
            score += 1
            target.generateNewCoord()
        elif score == 2 and len(balls) == 1:
            newBall = SeaUrchin(pRadius + 2, 5)
            newBall.createSeaUrchin()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 5 and len(balls) == 2:
            newBall = SeaUrchin(pRadius + 2, 6)
            newBall.createSeaUrchin()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 10 and len(balls) == 3:
            newBall = SeaUrchin(pRadius + 2, 7)
            newBall.createSeaUrchin()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 15 and len(balls) == 4:
            newBall = SeaUrchin(pRadius + 2, 8)
            newBall.createSeaUrchin()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 20 and len(balls) == 5:
            newBall = SeaUrchin(pRadius + 2, 9)
            newBall.createBall()
            balls.append(newBall)
            target.generateNewCoord()

        target.draw()
        displayScore()
        
        pygame.display.update()
        clock.tick(60)


def mainMenu():
    load_high_score()  # Load high score when the game starts
    # Load background image
    bg_image = pygame.image.load('men.png')
    bg_image = pygame.transform.scale(bg_image, (width, height))  # Scale image to fit the window

    font = pygame.font.SysFont("Elephant", 40)
    startText = font.render("Press 'S' to Start", True, (150, 200, 100))
    quitText = font.render("Press 'Q' to Quit", True, (150, 200, 100))
    
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                   gameLoop()
                if event.key == pygame.K_q:
                    close()

        # Draw background image
        display.blit(bg_image, (0, 0))

        # Render the menu text
        display.blit(startText, (85, 400))
        display.blit(quitText, (85, 350))

        pygame.display.update()
        clock.tick(60)

# Start the menu
mainMenu()
