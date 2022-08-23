class Player:
    
    def __init__(self, name: str):
        self.name = name
        self.is_dropped = False
        self.round_dropped = 0
        self.opponents = []
        self.points = 0
        self.pointrate = 0
        self.tiebreaker_1 = 0
        self.tiebreaker_2 = 0
        self.tiebreaker = 0

    def drop(self, round_nr: int):
        self.is_dropped = True
        self.round_dropped = round_nr
    
    def undrop(self, round_nr: int, win_bye: bool = False):
        self.is_dropped = False
        difference = round_nr - self.round_dropped
        for i in range(0, difference):
            self.opponents.append(Player("BYE"))
            if win_bye:
                self.add_win(i+1)
            else:
                self.add_loose(i+1)


    def add_win(self, round_nr: int):
        self.points += 3
        self.update_pointrate(round_nr)
        self.update_tiebreaker()

    def add_loose(self, round_nr: int):
        self.update_pointrate(round_nr)
        self.update_tiebreaker()

    def add_draw(self, round_nr: int):
        self.points += 1
        self.update_pointrate(round_nr)
        self.update_tiebreaker()

    def update_pointrate(self, round_nr: int):
        self.pointrate = round(self.points/float(round_nr * 3)*1000)
        if self.pointrate >= 1000:
            self.pointrate = 999

    def update_tiebreaker_1(self):
        if len(self.opponents) == 0:
            return
        percentage = 0
        counter = 0
        for p in self.opponents:
            if p.name != "BYE":
                percentage += p.pointrate
                counter += 1
        if counter > 0:
            self.tiebreaker_1 = round(percentage/float(counter))
        else:
            self.tiebreaker_1 = 0
        self.update_tiebreaker()

    def update_tiebreaker_2(self):
        if len(self.opponents) == 0:
            return
        percentage = 0
        counter = 0
        for p in self.opponents:
            if p.name != "BYE":
                percentage += p.tiebreaker_1
                counter += 1
        if counter > 0:
            self.tiebreaker_2 = round(percentage/float(counter))
        else:
            self.tiebreaker_2 = 0
        self.update_tiebreaker()

    def update_tiebreaker(self):
        self.tiebreaker = self.points * 1000000 + self.tiebreaker_1 * 1000 + self.tiebreaker_2
    
    def add_opponent(self, player):
        self.opponents.append(player)
    
    def __str__(self):
        return self.name
