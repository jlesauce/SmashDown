from typing import Any

from smashdown.tournament.match import Match
from smashdown.tournament.matcher.matcher_factory import MatcherFactory
from smashdown.tournament.pairing_method import PairingMethod
from smashdown.tournament.player import Player


class Tournament:
    def __init__(self, players: list[Player]):
        self.players = players
        self.teams = None

    def create_matches(self, pairing_method=PairingMethod.RANDOM) -> list[Match]:
        matcher = MatcherFactory.create_matcher(pairing_method)
        self.teams = matcher.match(self.players)

        for team in self.teams:
            self._update_partners(team.players[0], team.players[1])

        return self._create_matches_using_current_player_order()

    def _create_matches_using_current_player_order(self):
        num_matches = len(self.teams) // 2
        matches = []
        for match_index in range(num_matches):
            match = Match(self.teams[match_index * 2], self.teams[match_index * 2 + 1])
            matches.append(match)

        return matches

    @staticmethod
    def _update_partners(player1: Player, player2: Player) -> None:
        player1.add_partner(player2)
        player2.add_partner(player1)

    @staticmethod
    def _find_next_player_never_played_with(player: Player, players_queue: list[Player]) -> Any | None:
        for possible_player in players_queue:
            if player != possible_player and not possible_player.has_played_with(player):
                return possible_player
        return None
