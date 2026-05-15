class Rules:
    def __init__(self):
        pass

    def get_dice_values(self, cup):
        #Sammelt die 5 Zahlen aus dem Becher in eine einfache Liste
        werte = []
        for dice in cup.dice_list:
            werte.append(dice.value)
        return werte

    def check_number(self, dice_values, check_val):
        summe = 0
        for val in dice_values:
            if val == check_val:
                summe += val
        return summe

    def check_dreierpasch(self, dice_values):
        for i in range(1, 7):
            if dice_values.count(i) >= 3:
                return sum(dice_values)
        return 0

    def check_viererpasch(self, dice_values):
        for i in range(1, 7):
            if dice_values.count(i) >= 4:
                return sum(dice_values)
        return 0

    def check_full_house(self, dice_values):
        hat_drei = False
        hat_zwei = False
        for i in range(1, 7):
            if dice_values.count(i) == 3:
                hat_drei = True
            if dice_values.count(i) == 2:
                hat_zwei = True
            if dice_values.count(i) == 5:
                return 25 # Ein Kniffel ist auch ein Full House
                
        if hat_drei and hat_zwei:
            return 25
        return 0

    def check_kleine_strasse(self, dice_values):
        #Sortieren und doppelte entfernen
        sortiert = sorted(list(set(dice_values)))
        
        #In einen Text umwandeln (z.B. [1,2,3,4] wird zu "1234")
        text = ""
        for zahl in sortiert:
            text += str(zahl)
            
        if "1234" in text or "2345" in text or "3456" in text:
            return 30
        return 0

    def check_grosse_strasse(self, dice_values):
        sortiert = sorted(list(set(dice_values)))
        text = ""
        for zahl in sortiert:
            text += str(zahl)
            
        if "12345" in text or "23456" in text:
            return 40
        return 0

    def check_kniffel(self, dice_values):
        for i in range(1, 7):
            if dice_values.count(i) == 5:
                return 50
        return 0

    def check_chance(self, dice_values):
        return sum(dice_values)