import logging

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMainWindow
from observable import Observable

from smashdown.application_model import ApplicationModel

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    EVENT_ID_ON_CLOSE_BUTTON_CLICKED = 'close_event'
    EVENT_ID_ON_START_TOURNAMENT_BUTTON_CLICKED = 'start_tournament'

    def __init__(self, model: ApplicationModel):
        super().__init__()
        self._model = model
        self._event_listeners = Observable()

        self._init_ui()

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
        self.setGeometry(200, 200, 300, 150)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        self._create_labels_and_input_fields(grid_layout)
        self._create_start_button(grid_layout)

    def _create_labels_and_input_fields(self, layout):
        num_teams_label = QLabel('Number of teams:')
        self.num_teams_input = QLineEdit()
        num_rounds_label = QLabel('Number of rounds:')
        self.num_rounds_input = QLineEdit()

        layout.addWidget(num_teams_label, 0, 0)
        layout.addWidget(self.num_teams_input, 0, 1)
        layout.addWidget(num_rounds_label, 1, 0)
        layout.addWidget(self.num_rounds_input, 1, 1)

    def _create_start_button(self, layout):
        submit_button = QPushButton('Start tournament')
        submit_button.clicked.connect(self._on_click_start_tournament_button)
        layout.addWidget(submit_button, 2, 0, 1, 2)

    def _validate_input_fields(self):
        num_teams = self.num_teams_input.text()
        num_rounds = self.num_rounds_input.text()

        if not num_teams.isdigit() or not num_rounds.isdigit():
            self.show_error_message(message='Please enter valid numbers')
            return

    def _on_click_start_tournament_button(self):
        self._validate_input_fields()
        num_teams = int(self.num_teams_input.text())
        num_rounds = int(self.num_rounds_input.text())

        logger.debug(f'Notify {self.EVENT_ID_ON_START_TOURNAMENT_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_START_TOURNAMENT_BUTTON_CLICKED,
                                      num_teams=num_teams,
                                      num_rounds=num_rounds)
