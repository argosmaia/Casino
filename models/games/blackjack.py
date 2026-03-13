import random

class BlackjackModel:
    """ Lógica pura do Blackjack. Sem prints, sem drama. """
    def __init__(self):
        self.deck = self.get_deck()

    def get_deck(self):
        suits = ["♥️", "♦️", "♠️", "♣️"]
        ranks = [str(n) for n in range(2, 11)] + ['J', 'Q', 'K', 'A']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def get_valor_mao(self, cartas):
        valor = 0
        num_as = 0
        for carta in cartas:
            rank = carta[0]
            if rank == 'A':
                num_as += 1
            elif rank in ('K', 'Q', 'J'):
                valor += 10
            else:
                valor += int(rank)
        valor += num_as
        for _ in range(num_as):
            if valor + 10 <= 21:
                valor += 10
        return valor

    def start_game(self):
        self.deck = self.get_deck()
        return [self.deck.pop(), self.deck.pop()], [self.deck.pop(), self.deck.pop()]

    def hit(self, mao):
        mao.append(self.deck.pop())
        return mao
