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
        #5 Würfel nebeneinander erstellen (auf der rechten Seite)
        start_x = 420
        y_position = 200
        size = 60
        spacing = 10  #Abstand zwischen den Würfeln
        
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

###PLAYER###

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

###SCORECARD###

class Scorecard:
    def __init__(self):
        #Alle Felder/Möglichkeiten
        self.scores = {
            "einser": None,
            "zweier": None,
            "dreier": None,
            "vierer": None,
            "fuenfer": None,
            "sechser": None,
            "dreierpasch": None,
            "viererpasch": None,
            "full_house": None,
            "kleine_strasse": None,
            "grosse_strasse": None,
            "kniffel": None,
            "chance": None
        }

    def has_bonus(self):
        #Prüft, ob der Bonus (35 Punkte) erreicht wurde
        #Der Bonus wird gewährt, wenn die Summe der Zahlenfelder >= 63 ist
        oberer_teil = ["einser", "zweier", "dreier", "vierer", "fuenfer", "sechser"]
        summe_oben = 0
        for kategorie in oberer_teil:
            if self.scores[kategorie] is not None:
                summe_oben += self.scores[kategorie]
        
        return summe_oben >= 63

    def sum(self):
        #Berechnet die Gesamtpunktzahl
        gesamt = 0
        for punkte in self.scores.values():
            if punkte is not None:
                gesamt += punkte
                
        if self.has_bonus():
            gesamt += 35
            
        return gesamt

    def score_points_on_scorecard(self, kategorie, punkte):
        #Trägt Punkte in eine Kategorie ein, falls diese noch frei ist
        if self.scores[kategorie] is None:
            self.scores[kategorie] = punkte
            return True
        return False

    def draw(self, window):
        #Zeichnet den Hintergrund für das Scoreboard (linke Seite: x=0 bis 380)
        bg_rect = pygame.Rect(20, 20, 360, 560)
        pygame.draw.rect(window, (240, 240, 240), bg_rect) #hellgrauer Kasten
        pygame.draw.rect(window, (0, 0, 0), bg_rect, 3)    #schwarze Umrandung

        font = pygame.font.SysFont(None, 30)
        
        y_offset = 40  #Start-Höhe für die erste Zeile
        
        #Titel
        title_text = font.render("SCOREBOARD", True, (0, 0, 0))
        window.blit(title_text, (130, y_offset))
        y_offset += 40

        #Alle Kategorien durchgehen und zeichnen
        for kategorie, punkte in self.scores.items():
            #Namen der Kategorie aufhübschen (z.B. "dreier_pasch" -> "Dreierpasch")
            name_anzeige = kategorie.capitalize().replace("_", "")
            
            #Punkte zu String, falls None => Strich
            punkte_anzeige = str(punkte) if punkte is not None else "-"
            
            #Text für Name und Punkte generieren
            name_text = font.render(name_anzeige, True, (0, 0, 0))
            punkte_text = font.render(punkte_anzeige, True, (0, 0, 0))
            
            #Links den Namen blitten, rechts die Punkte
            window.blit(name_text, (40, y_offset))
            window.blit(punkte_text, (300, y_offset))
            
            y_offset += 30  #Abstand zur nächsten Zeile 

        #Gesamtpunktzahl
        y_offset += 20
        summe_text = font.render("Gesamt:", True, (0, 0, 0))
        summe_punkte_text = font.render(str(self.sum()), True, (0, 0, 0))
        window.blit(summe_text, (40, y_offset))
        window.blit(summe_punkte_text, (300, y_offset))

