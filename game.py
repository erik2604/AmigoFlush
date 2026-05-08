import pygame
import random

###GAME###

class Game:
    def __init__(self, players, cup, window):
        self.players = players
        self.cup = cup
        self.window = window

    def game_won(self):
        pass

    def play_turn(self):
        pass

###CUP###

class Cup:
    def __init__(self):
        self.dice_list = []
        #5 Würfel nebeneinander erstellen
        start_x = 100
        y_position = 200
        size = 80
        spacing = 20  #Abstand zwischen den Würfeln
        
        for i in range(5):
            x_position = start_x + i * (size + spacing)
            #Würfel erstellen: Startwert 1, im Becher (True), Größe, Farbe (Weiß), Position
            new_dice = Dice(1, True, size, (255, 255, 255), (x_position, y_position))
            self.dice_list.append(new_dice)

    def roll(self):
        #Geht durch jeden Würfel in der Liste und lässt ihn würfeln
        for current_dice in self.dice_list:
            current_dice.roll_dice()

    def show(self, window):
        #Geht durch jeden Würfel in der Liste und lässt ihn sich zeichnen
        for current_dice in self.dice_list:
            current_dice.show(window)

###DICE###

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


class Player:
    def __init__(self, name, dices):
        self.name = name
        self.dices = dices

    def update_score(self):
        pass

    def score_points_on_scorecard(self):
        pass

    def chose_dices(self):
        pass

    def reset(self):
        pass