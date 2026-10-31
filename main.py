import pygame
import time

pygame.init()

gameWindow = pygame.display.set_mode((800, 600))
gameWindow.fill((0,0,0))
pygame.display.set_caption("TEST WINDOW")

player = pygame.surface.Surface((100, 100))
player.fill((255, 255, 255))
player_x = 350
player_y = 250
player_vel_x = 0
player_vel_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)


    gameWindow.fill((0, 0, 0))

    gameWindow.blit(player, (player_x, player_y))

    pygame.display.flip()