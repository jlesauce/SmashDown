import logging
import math

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView

from smashdown.tournament.match import Match
from smashdown.ui.table.table_helpers import add_border_below_header_row

logger = logging.getLogger(__name__)


class RoundsTabPanel(QTabWidget):
    NUM_OF_TABLE_COLMUNS = 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_widget_tabs = []
        self.spinners_by_tabs = []
        self.scores_by_round = []

    def create_tab(self, matches: list[Match]):
        table_widget = self._create_round_matches_table_widget(matches)
        self.insertTab(len(self.table_widget_tabs), table_widget, f'Round {len(self.table_widget_tabs) + 1}')
        self.table_widget_tabs.append(table_widget)
        self.setCurrentIndex(self.count() - 1)

        self.scores_by_round.append(matches)

    def set_score_spinners_enabled(self, tab_index, is_enabled=True):
        for spinners_by_row in self.spinners_by_tabs[tab_index]:
            for spinner_in_row in spinners_by_row:
                spinner_in_row.lineEdit().setReadOnly(not is_enabled)
                spinner_in_row.setDisabled(not is_enabled)

    def get_current_index(self) -> int:
        return self.currentIndex()

    def _create_round_matches_table_widget(self, matches: list[Match]) -> QTableWidget:
        table_widget = QTableWidget()

        table_widget.setColumnCount(self.NUM_OF_TABLE_COLMUNS)
        table_widget.setRowCount(len(matches))

        column_headers = ['Team 1', 'Team 2', 'Set 1', '', 'Set 2', '', 'Set 3', '']
        table_widget.setHorizontalHeaderLabels(column_headers)
        add_border_below_header_row(table_widget)

        self._create_cell_elements(table_widget, matches)
        self._stretch_table_columns(table_widget)

        return table_widget

    def _create_cell_elements(self, table_widget: QTableWidget, matches: list[Match]):
        self.spinners_by_tabs.append([])

        for row_ in range(len(matches)):
            # Column 0: Team 1
            column_team_1 = QTableWidgetItem(f"{matches[row_].team1}")
            table_widget.setItem(row_, 0, column_team_1)
            column_team_1.setFlags(column_team_1.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsEnabled)

            # Column 1: Team 2
            column_team_2 = QTableWidgetItem(f"{matches[row_].team2}")
            table_widget.setItem(row_, 1, column_team_2)
            column_team_2.setFlags(column_team_2.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsEnabled)

            # Spinners for Sets 1, 2 and 3
            row_spinners = []
            for column in range(2, self.NUM_OF_TABLE_COLMUNS):
                spinner = QtWidgets.QSpinBox()
                table_widget.setCellWidget(row_, column, spinner)
                spinner.valueChanged.connect(lambda value, row=row_, tab_index=self.currentIndex() + 1, col=column:
                                             self._on_spinner_changed(row, col, tab_index, value))
                row_spinners.append(spinner)
            self.spinners_by_tabs[self.count()].append(row_spinners)

    @staticmethod
    def _stretch_table_columns(table: QTableWidget):
        header = table.horizontalHeader()
        for column_index in range(0, table.columnCount()):
            header.setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)
        for column_index in range(0, 2):
            header.setSectionResizeMode(column_index, QHeaderView.ResizeMode.ResizeToContents)

    def _on_spinner_changed(self, row, column, tab_index, value):
        match = self.scores_by_round[tab_index][row]
        set_index = self.translate_column_index_to_set_number(column)
        team_number = self.translate_column_index_to_team_number(column)

        logger.debug(f'Update match score ({match}): Set{set_index + 1}, Team{team_number + 1}: {value=}')
        match.set_scores[set_index][team_number] = value

    @staticmethod
    def translate_column_index_to_set_number(column: int) -> int:
        index = math.floor((column - 2) // 2)
        return index

    @staticmethod
    def translate_column_index_to_team_number(column: int) -> int:
        return 0 if (column - 2) % 2 == 0 else 1
