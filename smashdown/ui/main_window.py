import logging

from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMessageBox, QApplication
from observable import Observable

from smashdown.application_model import ApplicationModel
from smashdown.tournament.player import Player
from smashdown.ui.design.ui_design_file import UiDesignFile
from smashdown.ui.table.players_scores_table_controller import PlayersScoresTableController
from smashdown.ui.table.players_table_controller import PlayersTableController
from smashdown.ui.table.rounds_tab_panel import RoundsTabPanel

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    EVENT_ID_ON_CLOSE_BUTTON_CLICKED = 'close_event'
    EVENT_ID_ON_NEXT_ROUND_BUTTON_CLICKED = 'next_round'
    EVENT_ID_ON_VALIDATE_BUTTON_CLICKED = 'validate'

    def __init__(self, model: ApplicationModel):
        super().__init__()
        self._model = model
        self._event_listeners = Observable()

        uic.loadUi(UiDesignFile('main_window.ui').path, self)
        self._rounds_tab_panel = RoundsTabPanel()
        self._players_table_controller = PlayersTableController(self.players_table)
        self._scores_table_controller = PlayersScoresTableController(self.players_scores_table)
        self._init_ui()

    def add_event_listener(self, function, event_id: str):
        self._event_listeners.on(event_id, function)

    def closeEvent(self, event):
        logger.debug(f'Notify {self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED, event)
        event.accept()

    def add_new_round_to_matches_tab_widget(self):
        self._rounds_tab_panel.create_tab(self._model.get_current_matches())

    def get_players_list(self):
        return self._players_table_controller.get_players_list()

    def update_players_scores(self, players: list[Player]):
        self._scores_table_controller.update_players_scores(players)

    @staticmethod
    def show_error_message(message: str, title='Oups!'):
        box = QMessageBox()
        box.setWindowTitle(title)
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

    @staticmethod
    def set_waiting_cursor(is_enable: bool):
        if is_enable:
            QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()

    def _init_ui(self):
        self.setWindowTitle(self._model.application_name)
        self._init_ui_actions()
        self.tab_matches_layout.addWidget(self._rounds_tab_panel)

    def _init_ui_actions(self):
        self.menu_action_exit.triggered.connect(QApplication.instance().quit)
        self.add_player_button.clicked.connect(self._on_click_add_player_button)
        self.next_round_button.clicked.connect(self._on_click_next_round_button)
        self.validate_button.clicked.connect(self._on_click_validate_button)

    def _on_click_add_player_button(self):
        self._players_table_controller.insert_player_in_table()

    def _on_click_next_round_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_NEXT_ROUND_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_NEXT_ROUND_BUTTON_CLICKED)

    def _on_click_validate_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_VALIDATE_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_VALIDATE_BUTTON_CLICKED, self._rounds_tab_panel.currentIndex())
