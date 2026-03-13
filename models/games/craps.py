import random

class CrapsModel:
    """ Lógica do Craps. Dados e Points. """
    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def check_come_out(self, total):
        if total in (7, 11): return "WIN"
        if total in (2, 3, 12): return "LOSE"
        return "POINT"
