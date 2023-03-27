import logging

from smashdown.application_model import ApplicationModel
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

    def generate_matches(self):
        if not self._tournament:
            self._tournament = Tournament(self._model.players)
            self._debug_print_players()

        self._tournament.create_random_teams()
        self._debug_print_teams()
        self._tournament.create_random_matches()
        self._view.add_new_round_to_matches_tab_widget(self._tournament.matches)
        self._debug_print_matches()

    @staticmethod
    def close_application(_):
        logger.info('Close application')

    def _init_event_listeners(self):
        self._view.add_event_listener(self.close_application, MainWindow.EVENT_ID_ON_CLOSE_BUTTON_CLICKED)
        self._view.add_event_listener(self._on_generate_matches_button_clicked,
                                      MainWindow.EVENT_ID_ON_GENERATE_MATCHES_BUTTON_CLICKED)

    def _debug_print_players(self):
        players_str = '\n'.join(['\t' + str(player) for player in self._model.players])
        logger.debug(f'\nList of players:\n{players_str}')

    def _debug_print_teams(self):
        teams = self._tournament.teams
        teams_str = '\n'.join(['\t' + str(index) + ': ' + str(teams[index]) for index in range(len(teams))])
        logger.debug(f'\nTeams:\n{teams_str}')

    def _debug_print_matches(self):
        matches = self._tournament.matches
        matches_str = '\n'.join(['\t' + str(index) + ': ' + str(matches[index]) for index in range(len(matches))])
        logger.debug(f'\nMatches:\n{matches_str}')

    def _update_player_list_in_model(self, players: list):
        player_objects = list()
        for player in players:
            player_objects.append(Player(first_name=player[0], last_name=player[1]))
        self._model.players = player_objects

    def _on_generate_matches_button_clicked(self):
        logger.debug(f'Generate matches')
        self._update_player_list_in_model(self._view.get_players_list())
        self.generate_matches()
