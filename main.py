#To-do list: 1) Finish Main Menu, 2) Create a functional Game Over screen, 3) Create the main game loop

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

class Player():
    def __init__(self):
        self.body = [(220, 190), (250, 190), (280, 190), (310, 190)]
        self.shape = pygame.Surface((30, 30))
        self.shape.fill((0, 255, 0))
        self.head = pygame.Surface((30, 30))
        self.head.fill((0, 200, 0))
        self.dir = "RIGHT"

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

player = Player()

apple = pygame.surface.Surface((40, 40))
apple.fill((255, 0, 0))
apple_x = -100
apple_y = -100
apple_x_def = -100
apple_y_def = -100
apple_vel_x = 0
apple_vel_y = 0
apple_vel_y_def = 0

a = 1
b = 0

clock = pygame.time.Clock()

game_state = 0

""" def collision_detection():
    return (player_x <= (apple_x +int(apple.width)) and 
            (player_x + player.width) >= apple_x and 
            player_y <= (apple_y + apple.height + 5) and 
            (player_y + player.height) >= apple_y)
 """
while True:
    clock.tick(10)
    match game_state:
        case 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        apple_x = apple_x_def
                        apple_y = apple_y_def
                        apple_vel_y = apple_vel_y_def

                        game_state = 1

            welcomeText = fontH1.render("Snake Game", True, (0, 0, 0))

            if a > 0:
                playText = fontP.render("PRESS ENTER TO PLAY", True, (0, 0, 0))
            elif a < 0:
                playText = fontP.render("PRESS ENTER TO PLAY", True, (255, 255, 255))

            b += 1

            if b > 1000:
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
    

            player.move()
            
            """ if collision_detection():
                apple_y = random.randint(0, gameWindow.height - 50)
                apple_x = random.randint(0, gameWindow.width - 50) """
    
            
        case 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game_state = 0


    #Drawing

    if game_state == 0:
        gameWindow.fill((255, 255, 255))

        gameWindow.blit(welcomeText, (230, 50))
        gameWindow.blit(playText, (230, 450))

    elif game_state == 1:
        gameWindow.fill((0, 0, 0))

        for i in player.body[0:-1]:
            gameWindow.blit(player.shape, i)
        gameWindow.blit(player.head, player.body[-1])

        #DEBUG TEXT
        """ debugText0 = fontP.render(str(player_x), False, (255, 255, 255))
        debugText1 = fontP.render(str(player_y), True, (255, 255, 255))
        debugText2 = fontP.render(str(player_x_last), True, (255, 255, 255))
        debugText3 = fontP.render(str(player_y_last), True, (255, 255, 255))
        gameWindow.blit(debugText0, (0, 0))
        gameWindow.blit(debugText1, (0, 20))
        gameWindow.blit(debugText2, (0, 40))
        gameWindow.blit(debugText3, (0, 60)) """
            

        apple_x += apple_vel_x
        apple_y += apple_vel_y
        gameWindow.blit(apple, (apple_x, apple_y))

    elif game_state == 2:
        gameWindow.fill((150, 0, 0))

        #gameWindow.blit(game_over, (50, 200))

    pygame.display.flip()