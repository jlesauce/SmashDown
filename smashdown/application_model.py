from PyQt6.QtCore import QSettings


class ApplicationModel:
    APPLICATION_NAME = 'SmashDown'
    APPLICATION_SHORT_NAME = 'smashdown'

    def __init__(self):
        self.application_name = ApplicationModel.APPLICATION_NAME
        self.settings = QSettings(ApplicationModel.APPLICATION_SHORT_NAME)
        self._init_settings()
        self.players = []
        self.current_round = -1
        self.matches_by_rounds = []

    def get_current_matches(self):
        return self.matches_by_rounds[self.current_round]

    def _init_settings(self):
        self.settings.setValue('dummy/setting_name', 'value')
