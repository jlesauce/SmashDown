from smashdown.tournament.team import Team


class Match:
    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.set_scores = [[0, 0], [0, 0], [0, 0]]

    def __str__(self):
        return str(self.team1) + '  VERSUS  ' + str(self.team2)
