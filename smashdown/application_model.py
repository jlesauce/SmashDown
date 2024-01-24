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
        if len(self.matches_by_rounds) > 0:
            return self.matches_by_rounds[self.current_round]
        else:
            return []

    def is_first_round(self) -> bool:
        return self.current_round < 1

    def _init_settings(self):
        self.settings.setValue('tournament/pairing_method', 'round_robin')

    def get_setting(self, key):
        if not self.settings.contains(key):
            raise Exception(f"Setting key '{key}' not found")
        return self.settings.value(key)
