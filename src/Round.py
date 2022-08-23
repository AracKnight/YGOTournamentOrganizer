from argparse import ArgumentError
from Player import Player
from Match import Match
import random

class Round:

    def __init__(self, players: list, nr: int) -> None:
        self.tables = {}
        self.number = 0
        players_copy = players.copy()
        rem_list = []
        for p in players_copy:
            if p.is_dropped:
                rem_list.append(p)
        for e in rem_list:
            players_copy.remove(e)
        players_copy.sort(key=lambda player: (player.tiebreaker, random.randrange(0,10000)), reverse=True)
        j = 1
        for i in range(0, len(players_copy), 2):
            if i == len(players_copy) - 1:
                match = Match(players_copy[i], Player("BYE"))
                match.report_win(players_copy[i], nr)
            else:
                match = Match(players_copy[i], players_copy[i+1])
            self.tables[j] = match
            j += 1
        self.number = nr
    
    def report_win(self, table: int, player: Player):
        match = self.tables[table]
        if match.player_1 != player and match.player_2 != player:
            raise ArgumentError()
        match.report_win(player, self.number)

    def report_loose(self, table: int, player: Player):
        match = self.tables[table]
        if match.player_1 != player and match.player_2 != player:
            return
        if match.player_1 == player:
            player = match.player_2
        match.report_win(player)

    def report_draw(self, table: int):
        self.tables[table].report_draw(self.number)
    
    def is_finished(self):
        finished = True
        for t in self.tables:
            if not self.tables[t].is_finished():
                finished = False
                break
        return finished
    
    def __str__(self):
        ret_str = ""
        for (key, value) in self.tables.items():
            ret_str +="Table {0}: {1} vs. {2}\n".format(key, value.player_1, value.player_2)
        return ret_str
