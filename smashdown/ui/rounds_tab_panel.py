from PyQt6.QtCore import QSysInfo, Qt
from PyQt6.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView

from smashdown.tournament.match import Match


class RoundsTabPanel(QTabWidget):
    NUM_OF_TABLE_COLMUNS = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = []

    def create_tab(self, matches: list[Match]):
        table_widget = self._create_round_matches_table_widget(matches)
        self.insertTab(len(self.tabs), table_widget, f'Round {len(self.tabs) + 1}')
        self.tabs.append(table_widget)
        self.setCurrentIndex(self.count() - 1)

    def _create_round_matches_table_widget(self, matches: list[Match]) -> QTableWidget:
        table_widget = QTableWidget()

        table_widget.setColumnCount(self.NUM_OF_TABLE_COLMUNS)
        table_widget.setRowCount(len(matches))

        column_headers = ['Team 1', 'Team 2', 'Set 1', 'Set 2', 'Set 3']
        table_widget.setHorizontalHeaderLabels(column_headers)

        for row in range(len(matches)):
            # Column 0: Team 1
            column_team_1 = QTableWidgetItem(f"{matches[row].team1}")
            table_widget.setItem(row, 0, column_team_1)
            column_team_1.setFlags(column_team_1.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsEnabled)

            # Column 1: Team 2
            column_team_2 = QTableWidgetItem(f"{matches[row].team2}")
            table_widget.setItem(row, 1, column_team_2)
            column_team_2.setFlags(column_team_2.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsEnabled)

            for column in range(2, self.NUM_OF_TABLE_COLMUNS):
                item = QTableWidgetItem("")
                table_widget.setItem(row, column, item)

        self._strech_table_columns(table_widget)
        self.add_border_below_header_row(table_widget)

        return table_widget

    @staticmethod
    def _strech_table_columns(table: QTableWidget):
        header = table.horizontalHeader()
        for column_index in range(0, 2):
            header.setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

    @staticmethod
    def add_border_below_header_row(table: QTableWidget):
        if QSysInfo.productType() == "windows" and QSysInfo.productVersion() == "10":
            table.horizontalHeader().setStyleSheet(
                "QHeaderView::section{"
                "border-top:0px solid #D8D8D8;"
                "border-left:0px solid #D8D8D8;"
                "border-right:1px solid #D8D8D8;"
                "border-bottom: 1px solid #D8D8D8;"
                "background-color:white;"
                "padding:4px;"
                "}"
                "QTableCornerButton::section{"
                "border-top:0px solid #D8D8D8;"
                "border-left:0px solid #D8D8D8;"
                "border-right:1px solid #D8D8D8;"
                "border-bottom: 1px solid #D8D8D8;"
                "background-color:white;"
                "}")
