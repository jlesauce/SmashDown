import logging

from smashdown.application_model import ApplicationModel
from smashdown.ui.main_window import MainWindow

logger = logging.getLogger(__name__)


class ApplicationController:

    def __init__(self, model: ApplicationModel):
        self.model = model
        self.view = MainWindow(model)

    def start_application(self):
        self._init_event_listeners()
        self.view.show()

    @staticmethod
    def close_application(_):
        logger.info('Close application')

    def _init_event_listeners(self):
        self.view.add_event_listener(self.close_application, MainWindow.EVENT_ID_ON_CLOSE_BUTTON_CLICKED)
