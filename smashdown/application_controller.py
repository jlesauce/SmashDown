import logging

from smashdown.application_model import ApplicationModel
from smashdown.tournament.pairing_method import PairingMethod
from smashdown.tournament.player import Player
from smashdown.tournament.tournament import Tournament
from smashdown.ui.main_window import MainWindow

logger = logging.getLogger(__name__)


class ApplicationController:

    def __init__(self, model: ApplicationModel):
        self._model = model
        self._view = MainWindow(model)
        self._tournament = None

    def start_application(self):
        self._init_event_listeners()
        self._view.show()

    def _next_round(self):
        if not self._tournament:
            self._tournament = Tournament(self._model.players)
            self._debug_print_players()

        self._create_round_matches()

        self._view.add_new_round_to_matches_tab_widget()
        self._debug_print_teams()
        self._debug_print_matches()
        self._view.set_next_round_button_enabled(False)
        self._view.set_validate_button_enabled(True)

    def _validate_scores(self, round_index: int):
        self._update_player_ranks(round_index)
        self._view.set_validate_button_enabled(False)
        self._view.set_score_spinners_enabled(False)
        self._view.set_next_round_button_enabled(True)

    def _create_round_matches(self):
        self._model.current_round += 1
        pairing_method = PairingMethod.RANDOM if self._model.is_first_round() \
            else PairingMethod.to_enum(self._model.get_setting('tournament/pairing_method'))
        matches = self._tournament.create_matches(pairing_method)
        self._model.matches_by_rounds.append(matches)

    def _update_player_ranks(self, round_index: int):
        matches = self._model.matches_by_rounds[round_index]

        self._update_player_scores(matches)

        sorted_players = Player.sort_players_by_score(self._model.players)
        for ordered_player_index in range(len(sorted_players)):
            sorted_players[ordered_player_index].rank = ordered_player_index

        self._debug_print_players_by_rank()
        self._view.update_players_scores(self._model.players)

    @staticmethod
    def _update_player_scores(matches):
        for match in matches:
            points_per_rally_scores = match.compute_points_per_rally_scores()
            logger.debug(f'Match {match}: PPR={points_per_rally_scores}')

            for player in match.team1.players:
                player.score += points_per_rally_scores[0]
            for player in match.team2.players:
                player.score += points_per_rally_scores[1]

    @staticmethod
    def close_application(_):
        logger.info('Close application')

    def _init_event_listeners(self):
        self._view.add_event_listener(self.close_application, MainWindow.EVENT_ID_ON_CLOSE_BUTTON_CLICKED)
        self._view.add_event_listener(self._on_next_round_button_clicked,
                                      MainWindow.EVENT_ID_ON_NEXT_ROUND_BUTTON_CLICKED)
        self._view.add_event_listener(self._on_validate_button_clicked,
                                      MainWindow.EVENT_ID_ON_VALIDATE_BUTTON_CLICKED)

    def _debug_print_players(self):
        players_str = '\n'.join(['\t' + str(player) for player in self._model.players])
        logger.debug(f'\nList of players:\n{players_str}')

    def _debug_print_teams(self):
        teams = self._tournament.teams
        teams_str = '\n'.join(['\t' + str(index) + ': ' + str(teams[index]) for index in range(len(teams))])
        logger.debug(f'\nTeams:\n{teams_str}')

    def _debug_print_matches(self):
        matches = self._model.get_current_matches()
        matches_str = '\n'.join(['\t' + str(index) + ': ' + str(matches[index]) for index in range(len(matches))])
        logger.debug(f'\nMatches:\n{matches_str}')

    def _debug_print_players_by_rank(self):
        str_ = ''
        for player in Player.sort_players_by_rank(self._model.players):
            str_ += f"\t#{player.rank} : {player} (Score={player.score})\n"
        logger.debug(f'\nPlayers by rank:\n{str_}')

    def _update_player_list_in_model(self, players: list):
        logger.debug('Update player list in model')
        player_objects = list()
        for player in players:
            player_objects.append(Player(first_name=player[0], last_name=player[1]))
        self._model.players = player_objects

    def _on_next_round_button_clicked(self):
        logger.debug(f'Generate matches')
        if not self._model.players:
            self._update_player_list_in_model(self._view.get_players_list())
        self._next_round()

    def _on_validate_button_clicked(self, round_index: int):
        logger.debug(f'Validate round {round_index}')
        self._validate_scores(round_index)
