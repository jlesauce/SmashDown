from PyQt6.QtCore import QSysInfo
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


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


def insert_columns_in_table(table: QTableWidget, *colum_values):
    row_position = table.rowCount()
    table.insertRow(row_position)

    values_to_be_inserted = colum_values if len(colum_values) > 0 else ["", ""]

    if len(values_to_be_inserted) != table.columnCount():
        raise ValueError(f'Invalid number of columns to insert: expected number of columns is '
                         f'{table.columnCount()}, received {len(values_to_be_inserted)}')

    for column in range(table.columnCount()):
        table.setItem(row_position, column, QTableWidgetItem(str(values_to_be_inserted[column])))


def stretch_table_columns(table: QTableWidget):
    header = table.horizontalHeader()
    for column_index in range(0, table.columnCount()):
        header.setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)


def clear_table(table: QTableWidget):
    while table.rowCount() > 0:
        table.removeRow(0)
