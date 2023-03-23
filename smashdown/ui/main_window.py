import logging

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMainWindow
from observable import Observable

from smashdown.application_model import ApplicationModel

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    EVENT_ID_ON_CLOSE_BUTTON_CLICKED = 'close_event'

    def __init__(self, model: ApplicationModel):
        super().__init__()
        self._model = model
        self._observable = Observable()

        self._init_ui()

    def add_event_listener(self, function, event_id: str):
        self._observable.on(event_id, function)

    def closeEvent(self, event):
        logger.debug(f'Notify {self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED} received')
        self._observable.trigger(self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED, event)
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
        # Set window title and size
        self.setWindowTitle('ShuttleSmash')
        self.setGeometry(200, 200, 300, 150)

        # Create central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid = QGridLayout()
        central_widget.setLayout(grid)

        # Create labels and input fields
        num_teams_label = QLabel('Number of teams:')
        self.num_teams_input = QLineEdit()
        num_rounds_label = QLabel('Number of rounds:')
        self.num_rounds_input = QLineEdit()

        # Create submit button and connect to function
        submit_button = QPushButton('Start tournament')
        submit_button.clicked.connect(self.submit)

        # Add widgets to layout
        grid.addWidget(num_teams_label, 0, 0)
        grid.addWidget(self.num_teams_input, 0, 1)
        grid.addWidget(num_rounds_label, 1, 0)
        grid.addWidget(self.num_rounds_input, 1, 1)
        grid.addWidget(submit_button, 2, 0, 1, 2)

    def submit(self):
        # Get user input from input fields
        num_teams = self.num_teams_input.text()
        num_rounds = self.num_rounds_input.text()

        # Validate user input
        if not num_teams.isdigit() or not num_rounds.isdigit():
            QMessageBox.critical(self, 'Error', 'Please enter valid numbers')
            return

        # Convert user input to integers
        num_teams = int(num_teams)
        num_rounds = int(num_rounds)

        # Start tournament with user input
        # TODO: Add code to start tournament with user input
