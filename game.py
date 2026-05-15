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
        
        #Wenn der Würfel gesperrt ist (nicht im Becher), wird die Farbe leicht geändert, damit man sieht, dass er fixiert ist. 
        if self.in_cup == False:
            display_color = (200, 200, 200) #Grau
        else:
            display_color = self.color      #Weiß
            
        pygame.draw.rect(window, display_color, rect)
        
        #Umrandung (schwarz), damit er sich vom Hintergrund abhebt
        pygame.draw.rect(window, (0, 0, 0), rect, 2) 


        #Wert des Würfels anzeigen lassen
        font = pygame.font.SysFont(None, self.size)
        text = font.render(str(self.value), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + self.size/2, y + self.size/2))
        window.blit(text, text_rect)

###PLAYER###

class Player:
    def __init__(self, name):
        self.name = name
        #Jeder Spieler bekommt seine EIGENE Scorecard
        self.scorecard = Scorecard()
        #Ein Spieler darf im Kniffel genau 3 mal pro Runde würfeln
        self.rolls_left = 3

    def get_score(self):
        #Holt die aktuelle Gesamtpunktzahl von der eigenen Scorecard
        return self.scorecard.sum()

    def record_score(self, kategorie, punkte):
        #Trägt die Punkte auf die eigene Scorecard ein
        return self.scorecard.score_points_on_scorecard(kategorie, punkte)

    def reset_turn(self, cup):
        #Wird aufgerufen, wenn der Spieler seinen Zug beendet hat (Punkte wurden eingetragen)
        #1. Züge wieder auf 3 setzen
        self.rolls_left = 3
        #2. Alle Würfel wieder in den Becher legen (in_cup = True)
        for dice in cup.dice_list:
            dice.in_cup = True

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


def get_clicked_category(mouse_y):
    #Hilfsfunktion: Berechnet, auf welche Zeile geklickt wurde.
    #Die erste Zeile beginnt bei y=60, jede Zeile ist 28 Pixel hoch.
    start_y = 60
    row_height = 28
    
    #Reihenfolge der Kategorien, wie sie gezeichnet werden:
    kategorien = [
        "einser", "zweier", "dreier", "vierer", "fuenfer", "sechser",
        "dreierpasch", "viererpasch", "full_house", "kleine_strasse",
        "grosse_strasse", "kniffel", "chance"
    ]
    
    if mouse_y < start_y or mouse_y >= start_y + (len(kategorien) * row_height):
        return None #Außerhalb der Klick-Zone
        
    index = (mouse_y - start_y) // row_height
    return kategorien[index]


def draw_scoreboard(window, players, current_index):
    #Zeichnet den Hintergrund für das komplette Scoreboard
    bg_rect = pygame.Rect(10, 20, 390, 560)
    pygame.draw.rect(window, (240, 240, 240), bg_rect) # hellgrauer Kasten
    pygame.draw.rect(window, (0, 0, 0), bg_rect, 3)    # schwarze Umrandung

    font = pygame.font.SysFont(None, 24)
    font_bold = pygame.font.SysFont(None, 24, bold=True)
    
    y_offset = 30  # Start-Höhe
    
    #Kopfzeile mit Spielern (P1, P2, P3, P4)
    x_positions = [160, 220, 280, 340] #Spalten für die 4 Spieler
    for i, player in enumerate(players):
        #Aktiven Spieler rot markieren, die anderen schwarz
        color = (255, 0, 0) if i == current_index else (0, 0, 0)
        p_text = font_bold.render(f"P{i+1}", True, color)
        window.blit(p_text, (x_positions[i], y_offset))
        
    y_offset += 30

    #Alle Kategorien durchgehen.
    kategorien = list(players[0].scorecard.scores.keys())
    
    for kat in kategorien:
        #Kategorien-Name links
        name_anzeige = kat.capitalize().replace("_", " ")
        name_text = font.render(name_anzeige, True, (0, 0, 0))
        window.blit(name_text, (20, y_offset))
        
        #Punkte für jeden Spieler in seiner jeweiligen Spalte eintragen
        for i, player in enumerate(players):
            punkte = player.scorecard.scores[kat]
            punkte_anzeige = str(punkte) if punkte is not None else "-"
            punkte_text = font.render(punkte_anzeige, True, (0, 0, 0))
            window.blit(punkte_text, (x_positions[i] + 5, y_offset))
            
        y_offset += 28  # Abstand zur nächsten Zeile 

    #Gesamtpunktzahl am Ende
    y_offset += 20
    summe_text = font_bold.render("Gesamt:", True, (0, 0, 0))
    window.blit(summe_text, (20, y_offset))
    
    for i, player in enumerate(players):
        gesamt = player.scorecard.sum()
        gesamt_text = font_bold.render(str(gesamt), True, (0, 0, 0))
        window.blit(gesamt_text, (x_positions[i] + 5, y_offset))

