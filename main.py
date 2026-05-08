import game
import rules

import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))

#Becher erstellen
my_cup = game.Cup()
#Scoreboard erstellen
my_scorecard = game.Scorecard()

pygame.display.flip()

running=True
while running:
    #1. Benutzereingaben
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_cup.roll() #mischen
    #2. Zeichnen
    #Hintergrund zeichnen
    window.fill((100,20,120))

    #Becher inkl. Würfel zeichnen
    my_cup.show(window)
    
    #Scoreboard zeichnen
    my_scorecard.draw(window)

    #3. Anzeigen
    pygame.display.flip()

pygame.quit()

