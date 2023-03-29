from PyQt6.QtWidgets import QTableWidget, QAbstractItemView

from smashdown.tournament.player import Player
from smashdown.ui.table.table_helpers import insert_columns_in_table, add_border_below_header_row, clear_table, \
    stretch_table_columns


class PlayersScoresTableController:

    def __init__(self, table: QTableWidget):
        self.table = table
        self._init_table()

    def update_players_scores(self, players: list[Player]):
        clear_table(self.table)

        for player in Player.sort_players_by_rank(players):
            self._insert_player_score_in_table(str(player), round(player.score, 3))

        stretch_table_columns(self.table)

    def _insert_player_score_in_table(self, *colum_values):
        insert_columns_in_table(self.table, *colum_values)

    def _init_table(self):
        self.table.setHorizontalHeaderLabels(['Player', 'Score'])
        stretch_table_columns(self.table)
        add_border_below_header_row(self.table)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
