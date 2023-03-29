from smashdown.tournament.team import Team


class Match:
    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.set_scores = [[0, 0], [0, 0], [0, 0]]

    def compute_points_per_rally_scores(self) -> (float, float):
        total_rallies_played = sum([sum(score) for score in self.set_scores])
        if not total_rallies_played > 0:
            return 0.0, 0.0
        return (sum([score[0] for score in self.set_scores]) / total_rallies_played,
                sum([score[1] for score in self.set_scores]) / total_rallies_played)

    def __str__(self):
        return str(self.team1) + '  VERSUS  ' + str(self.team2)
