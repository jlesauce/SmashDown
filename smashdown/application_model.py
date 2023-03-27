from PyQt6.QtCore import QSettings


class ApplicationModel:
    APPLICATION_NAME = 'SmashDown'
    APPLICATION_SHORT_NAME = 'smashdown'

    def __init__(self):
        self.application_name = ApplicationModel.APPLICATION_NAME
        self.settings = QSettings(ApplicationModel.APPLICATION_SHORT_NAME)
        self._init_settings()
        self.players = []

    def _init_settings(self):
        self.settings.setValue('dummy/setting_name', 'value')
