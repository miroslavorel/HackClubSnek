#To-do list: 1) Finish Main Menu, 2) Create a functional Game Over screen, 3) Add snake getting longer

import pygame
import time
import random

pygame.init()
pygame.font.init()
fontH1 = pygame.font.SysFont("Cambria", 80)
fontP = pygame.font.SysFont("Cambria", 28)

gameWindow = pygame.display.set_mode((800, 600))
gameWindow.fill((0,0,0))
pygame.display.set_caption("TEST WINDOW")
bg = pygame.Surface((800, 600))
bg.fill((0, 0, 0))
bg = pygame.image.load("imgs/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (800, 600))

class Player():
    def __init__(self):
        self.body = [(220, 190), (250, 190), (280, 190), (310, 190)]
        self.shape = pygame.Surface((30, 30))
        self.shape.fill((0, 255, 0))
        self.head = pygame.Surface((30, 30))
        self.head.fill((0, 200, 0))
        self.dir = "RIGHT"
        self.score = 0

    def move(self):
        if self.dir == "RIGHT":
            self.body.append((self.body[len(self.body)-1][0] + 30 , self.body[len(self.body)-1][1]))
        elif self.dir == "UP":
            self.body.append((self.body[len(self.body)-1][0] , self.body[len(self.body)-1][1] - 30))
        elif self.dir == "DOWN":
            self.body.append((self.body[len(self.body)-1][0] , self.body[len(self.body)-1][1] + 30))
        elif self.dir == "LEFT":        
            self.body.append((self.body[len(self.body)-1][0] - 30 , self.body[len(self.body)-1][1]))
        self.body.pop(0)

    def self_collision(self):
        return self.body[-1] in self.body[0:-1]

    def wall_collision(self):
        return (self.body[-1][0] > gameWindow.width - 20 or 
        self.body[-1][0] < 10 or 
        self.body[-1][1] > gameWindow.height - 30 or 
        self.body[-1][1] < 10)

player = Player()

class Apple():
    def __init__(self):
        self.x = 190
        self.y = 160
        self.old_x = 190
        self.old_y = 160
        self.vel_x = 0
        self.vel_y = 0
        self.shape = pygame.Surface((20, 20))
        self.shape.fill((255, 0, 0))

    def getNewPos(self):
        while self.x == self.old_x:
            self.x += 1
            self.old_x += 1
            while self.x % 3 != 0:
                self.x = random.randint(1, int(gameWindow.width/10) - 4)
                self.x = self.x * 10
            
        while self.y == self.old_y:
            self.y += 1
            self.old_y += 1
            while self.y % 3 != 0:
                self.y = random.randint(1, int(gameWindow.height/10) - 4)
                self.y = self.y * 10
        self.x = self.x + 15    
        self.y = self.y + 15
        self.old_x = self.x
        self.old_y = self.y

apple = Apple()

a = 1
b = 0

clock = pygame.time.Clock()

debug = 1

game_state = 0

def apple_collision_detection():
    return (player.body[-1][0] <= (apple.x +int(apple.shape.width)) and 
            (player.body[-1][0] + player.shape.width) >= apple.x and 
            player.body[-1][1] <= (apple.y + apple.shape.height + 5) and 
            (player.body[-1][1] + player.shape.height) >= apple.y)

while True:
    clock.tick(10)
    match game_state:
        case 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player.body = [(220, 190), (250, 190), (280, 190), (310, 190)]
                        player.dir = "RIGHT"
                        apple.vel_x = 0
                        apple.vel_y = 0
                        apple.getNewPos()

                        game_state = 1

            welcomeText = fontH1.render("Snake Game", True, (0, 0, 0))

            if a > 0:
                playText = fontP.render("PRESS ENTER TO PLAY", True, (0, 0, 0))
            elif a < 0:
                playText = fontP.render("PRESS ENTER TO PLAY", True, (255, 255, 255))

            b += 1

            if b > 3:
                a = -a
                b = 0

        
        case 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if player.dir != "RIGHT" and player.dir != "LEFT":
                            player.dir = "LEFT"
                    elif event.key == pygame.K_RIGHT:
                        if player.dir != "LEFT" and player.dir != "RIGHT":
                            player.dir = "RIGHT"
                    elif event.key == pygame.K_UP:
                        if player.dir != "DOWN" and player.dir != "UP":
                            player.dir = "UP"
                    elif event.key == pygame.K_DOWN:
                        if player.dir != "UP" and player.dir != "DOWN":
                            player.dir = "DOWN"
                    elif event.key == pygame.K_BACKSPACE:
                        debug = -debug

            player.move()
            
            if apple_collision_detection():
                player.score += 1
                apple.getNewPos()

            if player.self_collision():
                time.sleep(1)
                game_state = 2

            if player.wall_collision():
                time.sleep(1)
                game_state = 2
    
            
        case 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = 0
            


    #Drawing

    #Main Menu Drawing
    if game_state == 0:
        gameWindow.fill((255, 255, 255))

        gameWindow.blit(welcomeText, (230, 50))
        gameWindow.blit(playText, (230, 450))

    #Main Game Loop Drawing
    elif game_state == 1:
        gameWindow.fill((0, 0, 0))
        
        gameWindow.blit(bg, (0, 0))


        for i in player.body[0:-1]:
            gameWindow.blit(player.shape, i)
        gameWindow.blit(player.head, player.body[-1])

        #DEBUG TEXT
        if debug < 0:
            debugText0 = fontP.render(str(player.body[-1][0]), False, (255, 255, 255))
            debugText1 = fontP.render(str(player.body[-1][1]), True, (255, 255, 255))
            debugText2 = fontP.render(str(apple.x), True, (255, 255, 255))
            debugText3 = fontP.render(str(apple.y), True, (255, 255, 255))
            gameWindow.blit(debugText0, (0, 0))
            gameWindow.blit(debugText1, (0, 20))
            gameWindow.blit(debugText2, (0, 40))
            gameWindow.blit(debugText3, (0, 60))
            debugText4 = fontP.render(str(apple.old_x), True, (255, 255, 255))
            debugText5 = fontP.render(str(apple.old_y), True, (255, 255, 255))
            gameWindow.blit(debugText4, (0, 80))
            gameWindow.blit(debugText5, (0, 100))
            #debugText6 = fontP.render(), True, (255, 255, 255))
            #gameWindow.blit(debugText6, (0, 120))
            

        apple.x += apple.vel_x
        apple.y += apple.vel_y
        gameWindow.blit(apple.shape, (apple.x, apple.y))

    #Game Over Screen Drawing
    elif game_state == 2:
        gameWindow.fill((0, 0, 0))

        if player.self_collision():
            collisionText = fontP.render("YOU COLIDED WITH YOURSELF", True, (255, 255, 255))
            gameWindow.blit(collisionText, (250, 250))

        if player.wall_collision():
            collisionText = fontP.render("YOU COLIDED WITH THE WALL", True, (255, 255, 255))
            gameWindow.blit(collisionText, (250, 250))

        #gameWindow.blit(game_over, (50, 200))

    pygame.display.flip()