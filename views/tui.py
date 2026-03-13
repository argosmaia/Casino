import os
import time

# Constantes de interface (Emojis que o Sr. Higgins odeia)
COPAS, OUROS, ESPADAS, PAUS = "♥️", "♦️", "♠️", "♣️"
GOLDEN_TADPOLE, DIAMOND, COIN, GRAPE, MELON, LEMON = "🐸", "💎", "🪙", "🍇", "🍉", "🍋"
BALL, MONEY_BAG, WARNING = "🎱", "💰", "⚠️"
BACKSIDE = 'backside'

class TUIView:
    """
    A cara do jogo. Se o terminal fosse um cinema, isso aqui seria o projetor.
    """
    @staticmethod
    def limpar_tela():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def mostrar_mensagem(msg, delay=0):
        print(msg)
        if delay > 0:
            time.sleep(delay)

    @staticmethod
    def prompt_input(texto):
        return input(f"{texto}\n> ")

    @staticmethod
    def mostrar_cartas(cartas):
        linhas = ['', '', '', '']
        for i, carta in enumerate(cartas):
            linhas[0] += ' ___  '
            if carta == BACKSIDE:
                linhas[1] += '|## | '
                linhas[2] += '|###| '
                linhas[3] += '|_##| '
            else:
                rank, suit = carta
                linhas[1] += '|{} | '.format(str(rank).ljust(2))
                linhas[2] += '| {} | '.format(suit)
                linhas[3] += '|_{}| '.format(str(rank).rjust(2, '_'))
        for linha in linhas:
            print(linha)

    @staticmethod
    def draw_dice(v1, v2):
        patterns = {
            1: ["       ", "   o   ", "       "],
            2: [" o     ", "       ", "     o "],
            3: [" o     ", "   o   ", "     o "],
            4: [" o   o ", "       ", " o   o "],
            5: [" o   o ", "   o   ", " o   o "],
            6: [" o   o ", " o   o ", " o   o "]
        }
        p1 = patterns[v1]
        p2 = patterns[v2]
        print("  -------     -------")
        for i in range(3):
            print(f" |{p1[i]}|   |{p2[i]}|")
        print("  -------     -------")

    @staticmethod
    def mostrar_keno_board():
        print("\n🎰 TABULEIRO KENO 🎰\n")
        for row in range(8):
            for col in range(10):
                num = row * 10 + col + 1
                print(f"| {num:2d} |", end="  ")
            print()
        print()
