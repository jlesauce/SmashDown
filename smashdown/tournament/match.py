from smashdown.tournament.team import Team


class Match:
    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.sets = list()

    def add_set(self, score_team1: int, score_team2: int):
        self.sets.append(Set(score_team1, score_team2))


class Set:
    def __init__(self, score_team1: int, score_team2: int):
        self.score_team1 = score_team1
        self.score_team2 = score_team2
