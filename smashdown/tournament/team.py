from typing import List

from smashdown.tournament.player import Player


class Team:
    def __init__(self, name: str, players: List[Player]):
        if len(players) != 2:
            raise ValueError('A team must contain exactly two players')

        self.name = name
        self.players = players
