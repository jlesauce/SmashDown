from abc import abstractmethod


class Matcher:

    @abstractmethod
    def match(self, players):
        pass
