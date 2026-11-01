import pygame
import time
import random

pygame.init()
pygame.font.init()
fontH1 = pygame.font.SysFont("Comic Sans MS", 60)
fontP = pygame.font.SysFont("Comic Sans MS", 28)

gameWindow = pygame.display.set_mode((800, 600))
gameWindow.fill((0,0,0))
pygame.display.set_caption("TEST WINDOW")

player = pygame.surface.Surface((100, 100))
player.fill((255, 255, 255))
player_x = 350
player_y = 250
player_x_def = 350
player_y_def = 250
player_vel_x = 0
player_vel_y = 0

fal_obj = pygame.surface.Surface((50, 50))
fal_obj.fill((255, 255, 255))
fal_obj_x = 0
fal_obj_y = 0
fal_obj_x_def = 0
fal_obj_y_def = 0
fal_obj_vel_x = 0
fal_obj_vel_y = 0.1
fal_obj_vel_y_def = 0.1

game_state = 0

def collision_detection():
    return (player_x <= (fal_obj_x +int(fal_obj.width)) and 
            (player_x + player.width) >= fal_obj_x and 
            player_y <= (fal_obj_y + fal_obj.height + 5) and 
            (player_y + player.height) >= fal_obj_y)

while True:
    match game_state:
        case 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_x = player_x_def
                        player_y = player_y_def

                        fal_obj_x = fal_obj_x_def
                        fal_obj_y = fal_obj_y_def
                        fal_obj_vel_y = fal_obj_vel_y_def

                        game_state = 1

            welcomeText = fontH1.render("Snake Game", False, (0, 0, 0))
        
        case 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_vel_x = -0.2
                    elif event.key == pygame.K_RIGHT:
                        player_vel_x = 0.2
                else:
                    player_vel_x = 0
                    player_vel_y = 0
    
            
            if collision_detection():
                fal_obj_y = 0
                fal_obj_x = random.randint(0, gameWindow.width - 50)
    
            if fal_obj_y >= 600:
                player_x, player_y = 1000, 1000
                player_vel_x, player_vel_y = 0, 0
    
                fal_obj_x, fal_obj_y = 1000, 1000
                fal_obj_vel_x, fal_obj_vel_y = 0, 0
    
                game_state = 2

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

        gameWindow.blit(welcomeText, (350, 250))

    elif game_state == 1:
        gameWindow.fill((0, 0, 0))

        player_x += player_vel_x
        player_y += player_vel_y
        gameWindow.blit(player, (player_x, player_y))

        fal_obj_x += fal_obj_vel_x
        fal_obj_y += fal_obj_vel_y
        gameWindow.blit(fal_obj, (fal_obj_x, fal_obj_y))

    elif game_state == 2:
        gameWindow.fill((150, 0, 0))

        #gameWindow.blit(game_over, (50, 200))

    pygame.display.flip()