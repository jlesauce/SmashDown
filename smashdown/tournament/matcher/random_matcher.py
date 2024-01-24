import random

from smashdown.tournament.matcher.matcher import Matcher
from smashdown.tournament.player import Player
from smashdown.tournament.team import Team


class RandomMatcher(Matcher):

    def match(self, players: list[Player]) -> list[Team]:
        random.shuffle(players)
        teams = []
        for team_index in range(len(players) // 2):
            player1, player2 = players[team_index * 2], players[team_index * 2 + 1]
            teams.append(Team([player1, player2]))

        return teams
