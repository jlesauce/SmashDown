from PyQt6.QtWidgets import QTableWidget

from smashdown.ui.table.table_helpers import add_border_below_header_row, insert_columns_in_table, stretch_table_columns


class PlayersTableController:

    def __init__(self, table: QTableWidget):
        self.table = table
        self._init_table()

    def get_players_list(self):
        table_content = []
        for row in range(self.table.rowCount()):
            row_content = []
            for column in range(self.table.columnCount()):
                cell = self.table.item(row, column)
                if cell is not None:
                    row_content.append(cell.text())
                else:
                    row_content.append('')
            table_content.append(row_content)
        return table_content

    def insert_player_in_table(self, *colum_values):
        insert_columns_in_table(self.table, *colum_values)

    def _init_table(self):
        self.table.setHorizontalHeaderLabels(['First Name', 'Last Name'])
        stretch_table_columns(self.table)
        add_border_below_header_row(self.table)

        # FIXME Remove after testing
        # + set default row to 1 in .ui file after removing this block
        self.insert_player_in_table('John', 'Shepard')
        self.insert_player_in_table('Jacques', 'Chirac')
        self.insert_player_in_table('Brigitte', 'Bardot')
        self.insert_player_in_table('Jean-Jacques', 'Goldman')
        self.insert_player_in_table('Emmanuel', 'Macron')
        self.insert_player_in_table('Ada', 'Lovelace')
        self.insert_player_in_table('Simone', 'Veil')
        self.insert_player_in_table('Mahatma', 'Gandhi')
        self.insert_player_in_table('Charles', 'De Gaulle')
        self.insert_player_in_table('Asterix', 'Le Gaulois')
        self.insert_player_in_table('Jack', "O'Neill")
        self.insert_player_in_table('Samantha', 'Carter')
        # FIXME END
