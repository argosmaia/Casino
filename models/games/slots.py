import random

class SlotsModel:
    """ Lógica dos Slots. 🐸💎🪙🍇🍉🍋 """
    SYMBOLS = ["🐸", "💎", "🪙", "🍇", "🍉", "🍋"]
    PAYOUTS = {
        ("🐸", "🐸", "🐸"): 20, ("💎", "💎", "💎"): 18, ("🪙", "🪙", "🪙"): 15,
        ("🍇", "🍇", "🍇"): 12, ("🍉", "🍉", "🍉"): 10, ("🍋", "🍋", "🍋"): 8,
        ("🐸", "🐸"): 5, ("💎", "💎"): 4, ("🪙", "🪙"): 3,
        ("🐸", "💎", "🪙"): 6, ("🍇", "🍉", "🍋"): 3
    }
    PENALTIES = { ("🐸", "🪙", "🍋"): -5, ("💎", "🍇", "🍉"): -4 }

    def spin(self):
        return random.choice(self.SYMBOLS), random.choice(self.SYMBOLS), random.choice(self.SYMBOLS)

    def calculate_payout(self, result, bet):
        payout = 0
        for key, multiplier in self.PAYOUTS.items():
            if all(item in result for item in key) and len(key) == result.count(key[0]):
                payout = bet * multiplier
                break
        
        penalty = 0
        for key, loss in self.PENALTIES.items():
            if sorted(key) == sorted(result):
                penalty = loss
                break
        
        return payout, penalty
