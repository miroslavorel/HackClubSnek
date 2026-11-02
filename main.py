#To-do list: 1) Finish Main Menu, 2) Finish Game Over screen

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

    def get_longer(self):
        self.body.insert(0, self.body[0])

    def apple_collision_detection(self):
        return (self.body[-1][0] <= (apple.x +int(apple.shape.width) + 2) and #had x menší než jablko x plus jeho fyzická velikost
            (self.body[-1][0] + self.shape.width + 2) >= apple.x and #had a jeho fyzická šířka větší než x jablka
            self.body[-1][1] <= (apple.y + apple.shape.height + 5 + 2) and #had y menší než jabko x a jeho výška plus 5
            (self.body[-1][1] + self.shape.height + 2) >= apple.y) #had y a jeho fyzická výška větší než y jablka

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
        while True:
            self.x = random.randint(1, 24) * 30 + 15
            self.y = random.randint(1, 18) * 30 + 15
            
            collision = False
            for segment in player.body:
                if (self.x < segment[0] + 30 and self.x + 20 > segment[0] and
                    self.y < segment[1] + 30 and self.y + 20 > segment[1]):
                    collision = True
                    break 

            if not collision and (self.x != self.old_x or self.y != self.old_y):
                self.old_x = self.x
                self.old_y = self.y
                break

apple = Apple()

a = 1
b = 0

clock = pygame.time.Clock()

debug = 1

game_state = 0


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
                        player.score = 0
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
            
            if player.apple_collision_detection():
                player.score += 10
                player.get_longer()
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
            

        apple.x += apple.vel_x
        apple.y += apple.vel_y
        gameWindow.blit(apple.shape, (apple.x, apple.y))

        scoreText = fontH1.render(str(player.score), True, (255, 255, 255))
        gameWindow.blit(scoreText, (10, 10))

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