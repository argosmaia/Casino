import random

class KenoModel:
    """ Lógica do Keno. 80 números de pura diversão. """
    NUM_RANGE = 80
    DRAW_COUNT = 20
    PAYOUTS = {
        1: {0: 0, 1: 2}, 2: {0: 0, 1: 1, 2: 5}, 3: {0: 0, 1: 1, 2: 2, 3: 10},
        4: {0: 0, 1: 1, 2: 1, 3: 5, 4: 25}, 5: {0: 0, 1: 1, 2: 1, 3: 2, 4: 15, 5: 50},
        6: {0: 0, 1: 1, 2: 1, 3: 1, 4: 5, 5: 30, 6: 75},
    }

    def draw(self):
        return random.sample(range(1, self.NUM_RANGE + 1), self.DRAW_COUNT)

    def calculate_hits(self, player_numbers, drawn_numbers):
        return len(set(player_numbers) & set(drawn_numbers))

    def get_payout(self, num_choices, hits, bet):
        return self.PAYOUTS.get(num_choices, {}).get(hits, 0) * bet
