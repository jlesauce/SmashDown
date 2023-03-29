class Player:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + ' ' + last_name.upper()
        self.score = 0
        self.rank = 0

    @staticmethod
    def sort_players_by_score(players: list, is_descending_order=True):
        return sorted(players, key=lambda p: p.score, reverse=is_descending_order)

    @staticmethod
    def sort_players_by_rank(players: list, is_descending_order=False):
        return sorted(players, key=lambda p: p.rank, reverse=is_descending_order)

    def __str__(self):
        return self.full_name
