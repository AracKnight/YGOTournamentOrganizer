from argparse import ArgumentError
from pickle import EMPTY_TUPLE
from Player import Player

class Match:
    
    def __init__(self, player_1: Player, player_2: Player) -> None:
        self.is_drawn = False
        self.winner = None
        self.player_1 = player_1
        self.player_2 = player_2
        player_1.add_opponent(player_2)
        player_2.add_opponent(player_1)
    
    def report_win(self, player: Player, round_nr: int):
        if self.player_1 != player and self.player_2 != player:
            raise ArgumentError()
        self.winner = player
        player.add_win(round_nr)
        if self.player_1 == player:
            self.player_2.add_loose(round_nr)
        else:
            self.player_1.add_loose(round_nr)

    def report_draw(self, round_nr: int):
        self.is_drawn = True
        self.player_1.add_draw(round_nr)
        self.player_2.add_draw(round_nr)

    def is_finished(self):
        return self.is_drawn or self.winner
