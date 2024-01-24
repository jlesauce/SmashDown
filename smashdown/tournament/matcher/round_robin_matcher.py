from smashdown.tournament.matcher.matcher import Matcher
from smashdown.tournament.player import Player
from smashdown.tournament.team import Team


class RoundRobinMatcher(Matcher):

    def match(self, players: list[Player]) -> list[Team]:
        graph = self._create_graph(players)
        unplayed_pairs = self._find_unplayed_pairs(graph)

        teams = []
        for pair in unplayed_pairs:
            for team in teams:
                if pair[0] in team.players or pair[1] in team.players:
                    break
            else:
                teams.append(Team(pair))
        return teams
