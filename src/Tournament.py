from argparse import ArgumentError
from array import array
from xmlrpc.client import Boolean


from Player import Player
from Round import Round


class Tournament:

    def __init__(self, name: str = "", max_rounds: int = 9999):
        self.players = []
        self.rounds = []
        self.current_round = None
        self.max_rounds = max_rounds
        self.name = name

    def add_player(self, name: str, win_bye: Boolean = False):
        player = Player(name)
        if self.current_round:
            if self.current_round.number > 0:
                self.add_player_late(player, win_bye)
        else:
            self.players.append(player)
    
    def add_player_range(self, players: list, win_bye: bool = False):
        for p in players:
            self.add_player(p, win_bye)
    
    def add_player_late(self, player: Player, win_bye: bool = False):
        nr = self.current_round.number
        for i in range(1, nr+1):
            player.opponents.append(Player("BYE"))
            if win_bye:
                player.add_win(i)
            else:
                player.add_loose(i)

    def drop_player(self, name: str):
        player = self.get_player_by_name(name)
        player.drop()
    
    def undrop_player(self, name: str, win_bye: bool = False):
        player = self.get_player_by_name(name)
        player.undrop(win_bye)
    
    def pair_next_round(self):
        if self.current_round:
            if not self.current_round.is_finished():
                raise ArgumentError()
            nr = self.current_round.number + 1
        else:
            nr = 1
        for p in self.players:
            p.update_pointrate(nr)
        for p in self.players:
            p.update_tiebreaker_1()
        for p in self.players:
            p.update_tiebreaker_2()
        new_round = Round(self.players, nr)
        self.rounds.append(new_round)
        self.current_round = new_round
    
    def report_win(self, table: int, name: str):
        player = self.get_player_by_name(name)
        if not player:
            raise ArgumentError()
        self.current_round.report_win(table, player)

    def report_loose(self, table: int, name: str):
        player = self.get_player_by_name(name)
        if not player:
            return
        self.current_round.report_loose(table, player)

    def report_draw(self, table: int):
        self.current_round.report_draw(table)

    def get_player_by_name(self, name: str):
        for p in self.players:
            if p.name == name:
                return p
        return None
    
    def get_standings(self):
        standings = ""
        if self.current_round:
            if not self.current_round.is_finished():
                return standings
        else:
            return standings
        for p in self.players:
            p.update_pointrate(self.current_round.number)
        for p in self.players:
            p.update_tiebreaker_1()
        for p in self.players:
            p.update_tiebreaker_2()
        self.players.sort(key=lambda player: player.tiebreaker, reverse=True)
        j = 1
        last_tie = -1
        for p in self.players:
            if last_tie == p.tiebreaker:
                standings += "\t{0}\t{1}\n".format(p.name, p.tiebreaker)
            else:
                last_tie = p.tiebreaker
                standings += "{0}\t{1}\t{2}\n".format(j, p.name, p.tiebreaker)
            j += 1
        return standings
