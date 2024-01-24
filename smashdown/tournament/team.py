from typing import Iterable

from smashdown.tournament.player import Player


class Team:
    def __init__(self, players: Iterable[Player]):
        if len(players) != 2:
            raise ValueError('A team must contain exactly two players')
        self.players = players

    def __str__(self):
        return ' / '.join([str(player) for player in self.players])
