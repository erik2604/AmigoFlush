from dice import Dice

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