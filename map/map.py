from pyexpat.errors import XML_ERROR_INVALID_TOKEN
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1024,1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Summoner's Rift")
mapBackground = pygame.image.load('map/map11.png')

DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)
mapBackground = pygame.transform.smoothscale(mapBackground, DEFAULT_IMAGE_SIZE)

"""
WHITE = (255,255,255)
YELLOW = (255, 255,0)
BLUE = (0,0,255)
RED  = (188,39,50)
DARK_GREY = (61, 62,87)
"""
def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.blit(mapBackground, (0,0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
    pygame.quit()
