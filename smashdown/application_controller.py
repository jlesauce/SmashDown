import logging

from smashdown.application_model import ApplicationModel
from smashdown.tournament.tournament import Tournament
from smashdown.ui.main_window import MainWindow

logger = logging.getLogger(__name__)


class ApplicationController:

    def __init__(self, model: ApplicationModel):
        self._model = model
        self._view = MainWindow(model)

    def start_application(self):
        self._init_event_listeners()
        self._view.show()

    @staticmethod
    def close_application(_):
        logger.info('Close application')

    def _init_event_listeners(self):
        self._view.add_event_listener(self.close_application, MainWindow.EVENT_ID_ON_CLOSE_BUTTON_CLICKED)
        self._view.add_event_listener(self.on_start_tournament_button_clicked,
                                      MainWindow.EVENT_ID_ON_START_TOURNAMENT_BUTTON_CLICKED)

    @staticmethod
    def on_start_tournament_button_clicked(num_teams: int, num_rounds: int):
        logger.debug(f'Start tournament : {num_teams=}, {num_rounds=}')
        Tournament(num_teams, num_rounds)
