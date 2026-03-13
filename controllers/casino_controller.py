import sys
import os
import pygame
from models.player import Player
from models.games.blackjack import BlackjackModel
from models.games.slots import SlotsModel
from models.games.keno import KenoModel
from models.games.craps import CrapsModel
from views.tui import TUIView

class CasinoController:
    """
    O Cérebro do Cassino. Cara, ele resolve tudo, tipo eu no Billy Madison.
    """
    def __init__(self):
        self.player = Player.load()
        self.view = TUIView()
        self.bj_model = BlackjackModel()
        self.slots_model = SlotsModel()
        self.keno_model = KenoModel()
        self.craps_model = CrapsModel()
        pygame.mixer.init()

    def tocar_som(self, arquivo):
        try:
            caminho = os.path.join("music", arquivo)
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play()
        except:
            pass

    def run(self):
        while True:
            self.view.limpar_tela()
            print(f"\n🎲 BEM-VINDO AO CASSINO DO ADAM! 🎲")
            print(f"Seu saldo atual é de R$ {self.player.saldo}.")
            print(f"High Score: R$ {self.player.high_score}")
            print("\nEscolha um jogo:")
            print("1. Blackjack")
            print("2. Slots")
            print("3. Keno")
            print("4. Craps (Dados)")
            print("5. Salvar Jogo")
            print("6. Sair")
            
            escolha = self.view.prompt_input("O que vai ser, brother?")
            
            if escolha == "1": self.play_blackjack()
            elif escolha == "2": self.play_slots()
            elif escolha == "3": self.play_keno()
            elif escolha == "4": self.play_craps()
            elif escolha == "5":
                self.player.save()
                self.view.mostrar_mensagem("Jogo salvo! Agora pode dormir tranquilo.", 2)
            elif escolha == "6":
                self.player.save()
                self.view.mostrar_mensagem("Valeu por jogar! Até a próxima, dude.", 1)
                sys.exit()
            else:
                self.view.mostrar_mensagem("Escolha inválida. Tenta de novo!", 1)

    def get_bet(self):
        while True:
            bet = self.view.prompt_input(f"Quanto quer apostar? (1 - {self.player.saldo}) ou 'QUIT'")
            if bet.upper() == 'QUIT': return None
            if bet.isdecimal() and self.player.pade_apostar(int(bet)):
                return int(bet)
            self.view.mostrar_mensagem("Aposta inválida, cara!", 1)

    def play_blackjack(self):
        self.view.mostrar_mensagem("BLACKJACK! Tenta chegar no 21 sem explodir.", 1)
        bet = self.get_bet()
        if not bet: return

        banca_mao, jogador_mao = self.bj_model.start_game()
        while True:
            self.view.limpar_tela()
            print("Banca: ???")
            self.view.mostrar_cartas(['backside'] + banca_mao[1:])
            print(f"Jogador: {self.bj_model.get_valor_mao(jogador_mao)}")
            self.view.mostrar_cartas(jogador_mao)

            if self.bj_model.get_valor_mao(jogador_mao) > 21:
                self.tocar_som("perdeu.mp3")
                self.view.mostrar_mensagem("EXPLODIU! Você perdeu.", 2)
                self.player.remover_saldo(bet)
                return

            move = self.view.prompt_input("(H)it ou (S)tand?").upper()
            if move == 'H':
                self.bj_model.hit(jogador_mao)
            elif move == 'S':
                break

        while self.bj_model.get_valor_mao(banca_mao) < 17:
            self.bj_model.hit(banca_mao)

        self.view.limpar_tela()
        bv, jv = self.bj_model.get_valor_mao(banca_mao), self.bj_model.get_valor_mao(jogador_mao)
        print(f"Banca: {bv}")
        self.view.mostrar_cartas(banca_mao)
        print(f"Jogador: {jv}")
        self.view.mostrar_cartas(jogador_mao)

        if bv > 21 or jv > bv:
            self.tocar_som("ganhou.mp3")
            self.view.mostrar_mensagem(f"GANHOU! R$ {bet} na conta.", 2)
            self.player.adicionar_saldo(bet)
        elif jv < bv:
            self.tocar_som("perdeu.mp3")
            self.view.mostrar_mensagem("PERDEU! A banca levou essa.", 2)
            self.player.remover_saldo(bet)
        else:
            self.view.mostrar_mensagem("EMPATE! Dinheiro devolvido.", 2)

    def play_slots(self):
        bet = self.get_bet()
        if not bet: return
        self.tocar_som("Jackpot.mp3")
        self.view.mostrar_mensagem("Girando... 🎲", 1)
        res = self.slots_model.spin()
        print(f"🎰 | {res[0]} | {res[1]} | {res[2]} | 🎰")
        payout, penalty = self.slots_model.calculate_payout(res, bet)
        
        if payout > 0:
            self.tocar_som("ganhou.mp3")
            self.view.mostrar_mensagem(f"🎉 GANHOU R$ {payout}! 🎉", 2)
            self.player.adicionar_saldo(payout)
        elif penalty < 0:
            self.tocar_som("perdeu.mp3")
            self.view.mostrar_mensagem(f"💀 AZAR! Perdeu R$ {-penalty}!", 2)
            self.player.remover_saldo(-penalty)
        else:
            self.tocar_som("perdeu.mp3")
            self.view.mostrar_mensagem("Nada feito. Perdeu a aposta.", 2)
            self.player.remover_saldo(bet)

    def play_craps(self):
        bet = self.get_bet()
        if not bet: return
        
        self.view.prompt_input("Enter para lançar os dados... 🎲")
        d1, d2 = self.craps_model.roll_dice()
        total = d1 + d2
        self.view.draw_dice(d1, d2)
        status = self.craps_model.check_come_out(total)

        if status == "WIN":
            self.tocar_som("ganhou.mp3")
            self.view.mostrar_mensagem(f"NATURAL! Ganhou R$ {bet}!", 2)
            self.player.adicionar_saldo(bet)
        elif status == "LOSE":
            self.tocar_som("perdeu.mp3")
            self.view.mostrar_mensagem(f"CRAPS! Perdeu R$ {bet}.", 2)
            self.player.remover_saldo(bet)
        else:
            point = total
            self.view.mostrar_mensagem(f"🎯 Point é {point}. Vamos lá!", 1)
            while True:
                self.view.prompt_input(f"Enter para tentar o {point}...")
                d1, d2 = self.craps_model.roll_dice()
                nt = d1 + d2
                self.view.draw_dice(d1, d2)
                if nt == point:
                    self.tocar_som("ganhou.mp3")
                    self.view.mostrar_mensagem(f"NA MOSCA! Ganhou R$ {bet}!", 2)
                    self.player.adicionar_saldo(bet)
                    break
                elif nt == 7:
                    self.tocar_som("perdeu.mp3")
                    self.view.mostrar_mensagem(f"SETE FORA! Perdeu R$ {bet}.", 2)
                    self.player.remover_saldo(bet)
                    break

    def play_keno(self):
        self.view.mostrar_keno_board()
        bet = self.get_bet()
        if not bet: return
        
        try:
            nums = list(map(int, self.view.prompt_input("Escolha de 1 a 6 números (1-80) separados por espaço:").split()))
            if not (1 <= len(nums) <= 6) or any(n < 1 or n > 80 for n in nums):
                raise ValueError
        except:
            self.view.mostrar_mensagem("Escolha inválida, dude!", 2)
            return

        drawn = self.keno_model.draw()
        print(f"Sorteados: {', '.join(map(str, sorted(drawn)))}")
        hits = self.keno_model.calculate_hits(nums, drawn)
        payout = self.keno_model.get_payout(len(nums), hits, bet)
        
        if payout > 0:
            self.tocar_som("ganhou.mp3")
            self.view.mostrar_mensagem(f"💰 GANHOU R$ {payout}! 💰", 2)
            self.player.adicionar_saldo(payout)
        else:
            self.tocar_som("perdeu.mp3")
            self.view.mostrar_mensagem("Não foi dessa vez...", 2)
            self.player.remover_saldo(bet)
