import itertools
import random
from typing import List, Tuple, Match

from smashdown.tournament.team import Team


class Tournament:
    def __init__(self, num_teams: int, num_rounds: int):
        self.num_teams = num_teams
        self.num_rounds = num_rounds
        self.teams = self._create_teams()
        self.matches = self._create_matches()

    def _create_teams(self) -> List[Team]:
        # TODO: Implement team creation logic to randomly pair players and assign to teams
        pass

    def _create_matches(self) -> List[Match]:
        if not self.teams:
            return None
        matches = []
        # Generate all possible combinations of teams and shuffle them
        combinations = list(itertools.combinations(self.teams, 2))
        random.shuffle(combinations)
        # Take the first num_rounds * num_teams/2 combinations
        combinations = combinations[:self.num_rounds * self.num_teams // 2]
        for team1, team2 in combinations:
            match = Match(team1, team2)
            matches.append(match)
        return matches

    def play(self):
        for match in self.matches:
            match.play()
            self.update_scores(match)

    def update_scores(self, match: Match):
        if match.score1 > match.score2:
            match.team1.score += 1
        elif match.score2 > match.score1:
            match.team2.score += 1

    def get_leaderboard(self) -> List[Tuple[str, int]]:
        leaderboard = []
        for team in self.teams:
            leaderboard.append((team.name, team.score))
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        return leaderboard
