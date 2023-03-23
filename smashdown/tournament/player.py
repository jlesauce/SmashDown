class Player:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + ' ' + last_name.upper()
        self.score = 0

    def __str__(self):
        return self.full_name
