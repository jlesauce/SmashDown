import argparse
import logging
import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication

from smashdown.application_controller import ApplicationController
from smashdown.application_model import ApplicationModel
from smashdown.utils.logger import configure_logger

logger = logging.getLogger(__name__)


def catch_exceptions(e, value, traceback):
    QtWidgets.QMessageBox.critical(None, "Critical Error", f"Exception: {e}\n\n"
                                                           f"{value}")
    old_hook(e, value, traceback)


# Redefine exception hook to catch PyQt exceptions
old_hook = sys.excepthook
sys.excepthook = catch_exceptions


def main():
    args = _parse_arguments()
    configure_logger(log_level=logging.getLevelName(args.log_level.upper()))

    app_model = ApplicationModel()
    logger.info(f'Start {app_model.application_name}')

    _create_ui(app_model)


def _create_ui(model: ApplicationModel):
    try:
        application = QApplication(sys.argv[:1])
        controller = ApplicationController(model)
        controller.start_application()
        sys.exit(application.exec())
    except Exception as e:
        logging.exception(e)


def _parse_arguments():
    parser = _create_argument_parser()
    return parser.parse_args()


def _create_argument_parser():
    parser = argparse.ArgumentParser(description=
                                     'SmashDown is a Python-based badminton tournament management system that helps '
                                     'organizers manage tournaments for double matches. The system generates random '
                                     'team pairings for each match, updates player rankings after each round, and '
                                     'ensures that each team plays against every other team exactly once.')
    parser.add_argument('--log-level', dest="log_level",
                        choices=['debug', 'info', 'warn', 'error', 'fatal'], default='info',
                        help="Set the application log level")
    return parser


if __name__ == "__main__":
    main()
