import game
import rules

import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))

#Becher erstellen
my_cup = game.Cup()

#Regeln-Objekt erstellen
my_rules = rules.Rules()

#Mehrere Spieler in einer Liste anlegen
players = [
    game.Player("Spieler 1"),
    game.Player("Spieler 2"),
    game.Player("Spieler 3"),
    game.Player("Spieler 4")
]
#Wer gerade dran ist (0 = Spieler 1, 1 = Spieler 2, ...)
current_player_index = 0
current_player = players[current_player_index]

pygame.display.flip()

running = True
while running:
    #1. Benutzereingaben
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #Nur würfeln, wenn der Spieler noch Würfe übrig hat
                if current_player.rolls_left > 0:
                    my_cup.roll() # mischen
                    current_player.rolls_left -= 1 #Einen Wurf abziehen
                    print(f"Gewürfelt! Noch {current_player.rolls_left} Würfe übrig.")
                    
            # PROVISORISCH: Mit der Enter-Taste beenden wir den Zug
            if event.key == pygame.K_RETURN:
                print(f"{current_player.name} beendet seinen Zug.")
                
                # 1. Wechseln zum nächsten Spieler in der Liste
                current_player_index = (current_player_index + 1) % len(players)
                current_player = players[current_player_index]
                
                # 2. Spieler und Becher für den Zug vorbereiten
                current_player.reset_turn(my_cup)
                print(f"Jetzt ist {current_player.name} dran!")

        #Wenn der Spieler mit der Maus klickt
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Position der Maus holen
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            clicked_dice = False
            #Prüfen, ob ein Würfel angeklickt wurde
            for dice in my_cup.dice_list:
                #Erstellt ein unsichtbares Rechteck exakt da, wo der Würfel ist
                dice_rect = pygame.Rect(dice.position[0], dice.position[1], dice.size, dice.size)
                
                #collidepoint prüft, ob der Klick (mouse_x, mouse_y) innerhalb des Würfel-Rechtecks war
                if dice_rect.collidepoint(mouse_x, mouse_y):
                    #Status umkehren: Wenn im Becher, dann raus (False); wenn draußen, dann wieder rein (True)
                    dice.in_cup = not dice.in_cup
                    clicked_dice = True
                    print(f"Würfel mit Wert {dice.value} ist nun {'im Becher' if dice.in_cup else 'draussen (gesperrt)'}")
                    
            # --- 2. Wurde auf das Scoreboard geklickt? ---
            #Wenn kein Würfel gesperrt ist und die Maus auf der linken Seite ist (x < 400)
            if not clicked_dice and mouse_x < 400:
                #Prüfen ob der Spieler mindestens einmal geklickt hat
                if current_player.rolls_left < 3:
                    clicked_category = game.get_clicked_category(mouse_y)
                    
                    if clicked_category is not None:
                        # 1. Die Würfelwerte holen (z.B. [3, 4, 3, 2, 5])
                        dice_vals = my_rules.get_dice_values(my_cup)
                        
                        # 2.Ausrechnen wie viele Punkte das gibt
                        points = 0
                        if clicked_category == "einser": points = my_rules.check_number(dice_vals, 1)
                        if clicked_category == "zweier": points = my_rules.check_number(dice_vals, 2)
                        if clicked_category == "dreier": points = my_rules.check_number(dice_vals, 3)
                        if clicked_category == "vierer": points = my_rules.check_number(dice_vals, 4)
                        if clicked_category == "fuenfer": points = my_rules.check_number(dice_vals, 5)
                        if clicked_category == "sechser": points = my_rules.check_number(dice_vals, 6)
                        if clicked_category == "dreierpasch": points = my_rules.check_dreierpasch(dice_vals)
                        if clicked_category == "viererpasch": points = my_rules.check_viererpasch(dice_vals)
                        if clicked_category == "full_house": points = my_rules.check_full_house(dice_vals)
                        if clicked_category == "kleine_strasse": points = my_rules.check_kleine_strasse(dice_vals)
                        if clicked_category == "grosse_strasse": points = my_rules.check_grosse_strasse(dice_vals)
                        if clicked_category == "kniffel": points = my_rules.check_kniffel(dice_vals)
                        if clicked_category == "chance": points = my_rules.check_chance(dice_vals)
                        
                        # 3. Eintragen auf der Scorecard
                        eingetragen = current_player.record_score(clicked_category, points)
                        
                        if eingetragen:
                            # 4. Nächster Spieler ist dran!
                            current_player_index = (current_player_index + 1) % len(players)
                            current_player = players[current_player_index]
                            
                            # 5. Becher und Würfel zurücksetzen
                            current_player.reset_turn(my_cup)
                        else:
                            print("Dieses Feld ist leider schon belegt!")
                else:
                    print("Du musst erst mindestens einmal würfeln!")

    #2. Zeichnen
    #Hintergrund zeichnen
    window.fill((100,20,120))

    #Becher inkl. Würfel zeichnen
    my_cup.show(window)
    
    #Komplettes Scoreboard von allen 4 Spielern zeichnen
    game.draw_scoreboard(window, players, current_player_index)

    #Anzeige wer dran ist und wie viele Würfe
    font = pygame.font.SysFont(None, 40)
    
    #Name des Spielers anzeigen
    name_text = font.render(f"Am Zug: {current_player.name}", True, (255, 255, 255))
    window.blit(name_text, (420, 50))
    
    #Verbleibende Würfe anzeigen
    info_text = font.render(f"Wuerfe uebrig: {current_player.rolls_left}", True, (255, 255, 255))
    window.blit(info_text, (420, 100))

    #3. Anzeigen
    pygame.display.flip()

pygame.quit()

