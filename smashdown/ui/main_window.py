import logging

from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox, QApplication
from observable import Observable

from smashdown.application_model import ApplicationModel
from smashdown.ui.design.ui_design_file import UiDesignFile
from smashdown.ui.rounds_tab_panel import RoundsTabPanel

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
        self._init_ui()

    def get_players_list(self):
        table_content = []
        players_table = self.players_table
        for row in range(players_table.rowCount()):
            row_content = []
            for column in range(players_table.columnCount()):
                cell = players_table.item(row, column)
                if cell is not None:
                    row_content.append(cell.text())
                else:
                    row_content.append('')
            table_content.append(row_content)
        return table_content

    def add_new_round_to_matches_tab_widget(self):
        self._rounds_tab_panel.create_tab(self._model.get_current_matches())

    def add_event_listener(self, function, event_id: str):
        self._event_listeners.on(event_id, function)

    def closeEvent(self, event):
        logger.debug(f'Notify {self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED, event)
        event.accept()

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
        self._init_players_table()
        self.tab_matches_layout.addWidget(self._rounds_tab_panel)

    def _init_ui_actions(self):
        self.menu_action_exit.triggered.connect(QApplication.instance().quit)
        self.next_round_button.clicked.connect(self._on_click_next_round_button)
        self.validate_button.clicked.connect(self._on_click_validate_button)

    def _init_players_table(self):
        players_table = self.players_table
        players_table.setHorizontalHeaderLabels(['First Name', 'Last Name'])
        self._strech_players_table_columns()
        RoundsTabPanel.add_border_below_header_row(players_table)

        # FIXME Remove after testing
        # + set default row to 1 in .ui file after removing this block
        self._insert_player_in_players_table_widget('John', 'Shepard')
        self._insert_player_in_players_table_widget('Jacques', 'Chirac')
        self._insert_player_in_players_table_widget('Brigitte', 'Bardot')
        self._insert_player_in_players_table_widget('Jean-Jacques', 'Goldman')
        self._insert_player_in_players_table_widget('Emmanuel', 'Macron')
        self._insert_player_in_players_table_widget('Ada', 'Lovelace')
        self._insert_player_in_players_table_widget('Simone', 'Veil')
        self._insert_player_in_players_table_widget('Mahatma', 'Gandhi')
        self._insert_player_in_players_table_widget('Charles', 'De Gaulle')
        self._insert_player_in_players_table_widget('Asterix', 'Le Gaulois')
        self._insert_player_in_players_table_widget('Jack', "O'Neill")
        self._insert_player_in_players_table_widget('Samantha', 'Carter')
        # FIXME END

        self.add_player_button.clicked.connect(self._on_click_add_player_button)

    def _strech_players_table_columns(self):
        header = self.players_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def _insert_player_in_players_table_widget(self, *colum_values):
        players_table = self.players_table
        row_position = players_table.rowCount()
        players_table.insertRow(row_position)

        values_to_be_inserted = colum_values if len(colum_values) > 0 else ["", ""]

        if len(values_to_be_inserted) != players_table.columnCount():
            raise ValueError(f'Invalid number of columns to insert: expected number of columns is '
                             f'{players_table.columnCount()}, received {len(values_to_be_inserted)}')

        for column in range(players_table.columnCount()):
            players_table.setItem(row_position, column, QTableWidgetItem(values_to_be_inserted[column]))

    def _on_click_add_player_button(self):
        self._insert_player_in_players_table_widget()

    def _on_click_next_round_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_NEXT_ROUND_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_NEXT_ROUND_BUTTON_CLICKED)

    def _on_click_validate_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_VALIDATE_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_VALIDATE_BUTTON_CLICKED, self._rounds_tab_panel.currentIndex())
