import cup
import dice
import game
import player
import rules
import scorecard

import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
window.fill((100,20,120))
pygame.display.flip()

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
pygame.quit()