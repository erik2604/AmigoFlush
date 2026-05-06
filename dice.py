import random
import pygame

class Dice:
    def __init__(self, value, in_cup, size, color, position):
        self.value = value
        self.in_cup = in_cup
        self.size = size
        self.color = color
        self.position = position

    def roll_dice(self):
        #Nur neu würfeln, wenn der Würfel nicht gesperrt ist
        if self.in_cup == True:
            self.value = random.randint(1,6)

    def show(self, window):
        x, y = self.position
        
        #Würfel als Rechteck zeichnen
        rect = pygame.Rect(x, y, self.size, self.size)
        pygame.draw.rect(window, self.color, rect)
        
        #Umrandung (schwarz), damit er sich vom Hintergrund abhebt
        pygame.draw.rect(window, (0, 0, 0), rect, 2) 


        #Wert des Würfels anzeigen lassen
        font = pygame.font.SysFont(None, self.size)
        text = font.render(str(self.value), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + self.size/2, y + self.size/2))
        window.blit(text, text_rect)