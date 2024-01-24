import itertools
from abc import abstractmethod

import networkx as nx

from smashdown.tournament.player import Player
from smashdown.tournament.team import Team


class Matcher:

    @abstractmethod
    def match(self, players: list[Player]) -> list[Team]:
        pass

    @staticmethod
    def _create_graph(players: list[Player]) -> nx.Graph:
        graph = nx.Graph()
        for player in players:
            graph.add_node(player, score=player.score)
            for opponent in player.previous_partners:
                graph.add_edge(player, opponent)
        return graph

    @staticmethod
    def _find_unplayed_pairs(graph: nx.Graph) -> list[tuple[Player, Player]]:
        unplayed_pairs = []
        for pair in itertools.combinations(graph.nodes, 2):
            if not graph.has_edge(*pair):
                unplayed_pairs.append(pair)
        return unplayed_pairs
