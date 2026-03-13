import json
import os

class Player:
    """
    Cara, esse é o Jogador. Ele guarda o seu suado dinheirinho.
    """
    def __init__(self, saldo_inicial=5000):
        self.saldo = saldo_inicial
        self.high_score = saldo_inicial

    def adicionar_saldo(self, valor):
        self.saldo += valor
        if self.saldo > self.high_score:
            self.high_score = self.saldo

    def remover_saldo(self, valor):
        self.saldo -= valor

    def pode_apostar(self, valor):
        return 1 <= valor <= self.saldo

    def save(self, filename="savegame.json"):
        """ Salva o estado do jogo. Tipo um checkpoint antes do boss. """
        data = {
            "saldo": self.saldo,
            "high_score": self.high_score
        }
        with open(filename, "w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls, filename="savegame.json"):
        """ Carrega o jogo. Se não tiver save, começa do zero (ou 5000). """
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                player = cls(data["saldo"])
                player.high_score = data.get("high_score", data["saldo"])
                return player
        return cls()
