import random

from smashdown.tournament.match import Match
from smashdown.tournament.player import Player
from smashdown.tournament.team import Team


class Tournament:
    def __init__(self, players: list[Player]):
        self.players = players
        self.num_players = len(players)
        self.teams = None
        self.matches = None

    def create_random_teams(self):
        random.shuffle(self.players)
        num_teams = self.num_players // 2
        teams = []
        for team_index in range(num_teams):
            team = Team([self.players[team_index * 2], self.players[team_index * 2 + 1]])
            teams.append(team)
        self.teams = teams

    def create_random_matches(self):
        if not self.teams:
            return

        random.shuffle(self.teams)
        num_matches = len(self.teams) // 2
        matches = []
        for match_index in range(num_matches):
            match = Match(self.teams[match_index * 2], self.teams[match_index * 2 + 1])
            matches.append(match)

        self.matches = matches
