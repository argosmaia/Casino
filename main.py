import random, sys, pygame

# Mixer para sons
pygame.mixer.init()

def tocarSom(arquivo):
    try:
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Erro ao tocar {arquivo}: {e}")

saldo = 5000  # Saldo global

COPAS = "♥️"
OUROS = "♦️"
ESPADAS = "♠️"
PAUS = "♣️"

# Emojis para representar os símbolos da slot machine
GOLDEN_TADPOLE = "🐸"
DIAMOND = "💎"
COIN = "🪙"
GRAPE = "🍇"
MELON = "🍉"
LEMON = "🍋"

# Emojis para o Keno 🎱
BALL = "🎱"
MONEY_BAG = "💰"
WARNING = "⚠️"

# Configuração do Keno
NUM_RANGE = 80  # Números de 1 a 80
DRAW_COUNT = 20  # Quantos números são sorteados

# Tabela de pagamentos (quantos acertos e o multiplicador)
PAYOUTS_KENO = {
    1: {0: 0, 1: 2},  # Se escolheu 1 número e acertou, ganha 2x
    2: {0: 0, 1: 1, 2: 5},  # Se escolheu 2, acertou 1 recebe aposta de volta
    3: {0: 0, 1: 1, 2: 2, 3: 10},
    4: {0: 0, 1: 1, 2: 1, 3: 5, 4: 25},
    5: {0: 0, 1: 1, 2: 1, 3: 2, 4: 15, 5: 50},
    6: {0: 0, 1: 1, 2: 1, 3: 1, 4: 5, 5: 30, 6: 75},
}

# Tabela de multiplicadores de vitória
PAYOUTS = {
    (GOLDEN_TADPOLE, GOLDEN_TADPOLE, GOLDEN_TADPOLE): 20,  # 🐸🐸🐸
    (DIAMOND, DIAMOND, DIAMOND): 18,  # 💎💎💎
    (COIN, COIN, COIN): 15,  # 🪙🪙🪙
    (GRAPE, GRAPE, GRAPE): 12,  # 🍇🍇🍇
    (MELON, MELON, MELON): 10,  # 🍉🍉🍉
    (LEMON, LEMON, LEMON): 8,  # 🍋🍋🍋
    (GOLDEN_TADPOLE, GOLDEN_TADPOLE): 5,  # 🐸🐸
    (DIAMOND, DIAMOND): 4,  # 💎💎
    (COIN, COIN): 3,  # 🪙🪙
    (GOLDEN_TADPOLE, DIAMOND, COIN): 6,  # 🐸💎🪙
    (GRAPE, MELON, LEMON): 3  # 🍇🍉🍋
}

# Penalidades que reduzem o saldo
PENALTIES = {
    (GOLDEN_TADPOLE, COIN, LEMON): -5,  # 🐸🪙🍋
    (DIAMOND, GRAPE, MELON): -4,  # 💎🍇🍉
}

# Todos os símbolos possíveis
SYMBOLS = [GOLDEN_TADPOLE, DIAMOND, COIN, GRAPE, MELON, LEMON]


BACKSIDE = 'backside'

def getBet(maxBet):
    # PERGUNTA AO JOGADOR O QUANTO ELE QUER GASTAR
    while True:
        print(f"Quanto quer apostar? 1 - {maxBet} or QUIT")
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print("Obrigado por jogar")
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet


def getDeck():
    deck = []
    for suit in (COPAS, OUROS, ESPADAS, PAUS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))

        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck


def mostrarMaos(jogadorMao, bancaMao, mostrarbancaMao):
    print()
    if mostrarbancaMao:
        print('Banca:', getValorMao(bancaMao))
        mostrarCartas(bancaMao)
    else:
        print('Banca: ???', getValorMao(bancaMao))
        mostrarCartas([BACKSIDE] + bancaMao[1:])

    print('JOGADOR:', getValorMao(jogadorMao))
    mostrarCartas(jogadorMao)


def getValorMao(cartas):
    valor = 0
    numdeAs = 0

    for carta in cartas:
        rank = carta[0]
        if rank == 'A':
            numdeAs += 1
        elif rank in ('K', 'Q', 'J'):
            valor += 10
        else:
            valor += int(rank)

    valor += numdeAs
    for i in range(numdeAs):
        if valor + 10 <= 21:
            valor += 10

    return valor

def mostrarCartas(cartas):
    linhas = ['', '', '', '']
    for i, carta in enumerate(cartas):
        linhas[0] += ' ___  '
        if carta == BACKSIDE:
            linhas[1] += '|## | '
            linhas[2] += '|###| '
            linhas[3] += '|_##| '
        else:
            rank, suit = carta
            linhas[1] += '|{} | '.format(rank.ljust(2))
            linhas[2] += '| {} | '.format(suit)
            linhas[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for linha in linhas:
        print(linha)


def getMovimento(jogadorMao, dinheiro):
    while True:
        movimentos = ['(H)it', '(S)tand']
        if len(jogadorMao) == 2 and dinheiro > 0:
            movimentos.append('(D)ouble down')
        moverPrompt = ', '.join(movimentos) + '> '
        movimento = input(moverPrompt).upper()
        if movimento in ('H', 'S'):
            return movimento
        if movimento == 'D' and '(D)ouble down' in movimentos:
            return movimento

def blackjack(dinheiro):
    print('''BLACKJACK também conhecido como 21 no Brasil.
        \nRegras do jogo:
        \nTente chegar a 21 pontos ou próximo disso sem que a banca chegue primeiro
        \nReis (K), Rainhas (Q) e Valetes (J) valem 10 pontos cada um
        \nÁs (A) valem 1 ou 11 pontos
        \nDe (H)it para pegar outra carta, de (S)tand para ficar com o naipe e parar o jogo
        \nNa sua primeira jogada, você pode (D)obrar para aumentar sua aposta, mas deve acertar exatamente mais uma vez antes de parar.
        \nEm caso de empate, a aposta é devolvida ao jogador. A banca para de bater quando soma 17''')

    while True:
        if dinheiro <= 0:
            print("PARECE-ME QUE TU ESTÁS QUEBRADO")
            print("POR SORTE NAO JOGASTE COM DINHEIRO DE VERDADE")
            print("VALEU POR JOGAR")
            return dinheiro  # Retorna o saldo atualizado

        print("Saldo: R$", dinheiro)
        bet = getBet(dinheiro)

        # DANDO AO JOGADOR E A BANCA DUAS CARTAS DA MESA
        deck = getDeck()
        bancaMao = [deck.pop(), deck.pop()]
        jogadorMao = [deck.pop(), deck.pop()]

        print("Aposta: R$", bet)
        while True:
            mostrarMaos(jogadorMao, bancaMao, False)
            print()

            if getValorMao(jogadorMao) > 21:
                tocarSom("perdeu.mp3")  # Som de derrota
                print("Voce perdeu... Banca estourada")
                dinheiro -= bet
                return dinheiro  # Retorna saldo atualizado

            movimento = getMovimento(jogadorMao, dinheiro - bet)

            if movimento == 'D':
                adicionalBet = getBet(min(bet, dinheiro - bet))
                bet += adicionalBet
                print(f"Aposta aumentada para R${bet:<.2f}")
                print("Aposta: R$", bet)

            if movimento in ('H', 'D'):
                novaCarta = deck.pop()
                rank, suit = novaCarta
                print(f"Voce pegou {rank} de {suit}")
                jogadorMao.append(novaCarta)
                if getValorMao(jogadorMao) > 21:
                    tocarSom("perdeu.mp3")  # Som de derrota
                    print("Voce perdeu... Banca estourada")
                    dinheiro -= bet
                    return dinheiro  # Retorna saldo atualizado

            if movimento in ('S', 'D'):
                break  # JOGADOR PARA DE JOGAR

        # Jogo da banca
        while getValorMao(bancaMao) < 17:
            print("A banca pega uma carta")
            bancaMao.append(deck.pop())
            mostrarMaos(jogadorMao, bancaMao, False)

            if getValorMao(bancaMao) > 21:
                tocarSom("ganhou.mp3")  # Som de vitória
                print("A banca ultrapassou 21 pontos")
                dinheiro += bet
                return dinheiro  # Retorna saldo atualizado
            input("Enter para continuar: ")
            print("\n\n")

        # FINAL DA RODADA
        mostrarMaos(jogadorMao, bancaMao, True)

        jogadorValor = getValorMao(jogadorMao)
        bancaValor = getValorMao(bancaMao)

        if bancaValor > 21:
            print(f"Banca estourada. Voce ganhou R${bet:<.2f}")
            dinheiro += bet

        elif (jogadorValor > 21) or (jogadorValor < bancaValor):
            tocarSom("perdeu.mp3")  # Som de derrota
            print("Tu perdestes")
            dinheiro -= bet

        elif jogadorValor > bancaValor:
            tocarSom("ganhou.mp3")  # Som de vitória
            print(f"Voce ganhou R${bet:<.2f}")
            dinheiro += bet

        elif jogadorValor == bancaValor:
            tocarSom("ganhou.mp3")  # Som de vitória
            print("Empate. Valor retornado")

        input("Enter para continuar")
        return dinheiro  # Retorna o saldo atualizado

def get_bet(saldo):
    """ Pergunta ao jogador quanto quer apostar. """
    while True:
        print(f"Quanto quer apostar? 1 - {saldo} ou QUIT")
        bet = input("> ").strip().upper()
        if bet == "QUIT":
            print("Obrigado por jogar! 🎰")
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= saldo:
            return bet


def spin_reels():
    """ Gira os rolos da slot machine e retorna um resultado. """
    return random.choice(SYMBOLS), random.choice(SYMBOLS), random.choice(SYMBOLS)


def slots(saldo):
    print("🎰 Bem-vindo ao Cassino Slots! 🎰\n")
    print("Tente a sorte e multiplique seu dinheiro! Boa sorte! 🍀\n")

    saldo = saldo

    while saldo > 0:
        print(f"Saldo: R$ {saldo}")
        bet = get_bet(saldo)

        # Rodando a máquina
        result = spin_reels()
        print("\n🎲 Girando... 🎲")
        print(f"🎰 | {result[0]} | {result[1]} | {result[2]} | 🎰\n")

        # Verificando ganhos
        payout = 0

        for key, multiplier in PAYOUTS.items():
            if all(item in result for item in key) and len(key) == result.count(key[0]):
                payout = bet * multiplier
                break

        # Verificando penalidades
        penalty = 0
        for key, loss in PENALTIES.items():
            if sorted(key) == sorted(result):
                penalty = loss
                break

        # Atualizando saldo
        if payout > 0:
            tocarSom("ganhou.mp3")  # Som de vitória
            print(f"🎉 Parabéns! Você ganhou R$ {payout} 🎉")
            saldo += payout
        elif penalty < 0:
            tocarSom("perdeu.mp3")  # Som de derrota
            print(f"💀 Azar! Você perdeu R$ {-penalty} 💀")
            saldo += penalty  # Penalidade reduz saldo
        else:
            tocarSom("perdeu.mp3")  # Som de derrota
            print("❌ Nada feito. Tente novamente! ❌")
            saldo -= bet  # Perde o valor apostado

        if saldo <= 0:
            tocarSom("perdeu.mp3")  # Som de derrota
            print("😢 Você ficou sem dinheiro! O jogo acabou. Obrigado por jogar! 🎰")
            sys.exit()

        input("\nPressione Enter para continuar...\n")
        return saldo

def get_bet(saldo):
    """ Pergunta ao jogador quanto quer apostar. """
    while True:
        print(f"Quanto quer apostar? 1 - {saldo} ou QUIT")
        bet = input("> ").strip().upper()
        if bet == "QUIT":
            print("Obrigado por jogar Keno! 🎱")
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= saldo:
            return bet


def print_keno_board():
    """ Exibe a matriz 8x10 com os números de 1 a 80. """
    print("\n🎰 TABULEIRO KENO 🎰\n")
    for row in range(8):  # 8 linhas
        for col in range(10):  # 10 colunas
            num = row * 10 + col + 1
            print(f"{num:2d}", end="  ")  # Imprime o número formatado
        print()  # Quebra de linha para próxima linha da matriz
    print()  # Espaço após matriz


def choose_numbers():
    """ Permite ao jogador escolher números para o Keno. """
    while True:
        print("Escolha de 1 a 6 números entre 1 e 80, separados por espaço:")
        try:
            numbers = list(map(int, input("> ").split()))
            if len(numbers) < 1 or len(numbers) > 6:
                raise ValueError("Escolha entre 1 e 6 números!")
            if any(n < 1 or n > 80 for n in numbers):
                raise ValueError("Todos os números devem estar entre 1 e 80!")
            return numbers
        except ValueError as e:
            print(f"{WARNING} Erro: {e}")


def draw_numbers():
    """ Sorteia os números vencedores. """
    return random.sample(range(1, NUM_RANGE + 1), DRAW_COUNT)


def keno(saldo):
    print("🎱 Bem-vindo ao Keno! 🎱\n")
    print("Escolha seus números, faça sua aposta e veja se a sorte está do seu lado! 🍀\n")

    saldo = saldo

    while saldo > 0:
        print(f"Saldo: R$ {saldo}\n")
        bet = get_bet(saldo)
        player_numbers = choose_numbers()

        print_keno_board()
        print("\n🎲 Sorteando os números... 🎲")
        drawn_numbers = draw_numbers()
        print(f"Números sorteados: {BALL} {', '.join(map(str, drawn_numbers))}\n")

        hits = len(set(player_numbers) & set(drawn_numbers))
        print(f"Você acertou {hits} números! 🎯")

        # Verifica o pagamento
        payout = PAYOUTS_KENO.get(len(player_numbers), {}).get(hits, 0) * bet

        if payout > 0:
            tocarSom("ganhou.mp3")  # Som de vitória
            print(f"{MONEY_BAG} Parabéns! Você ganhou R$ {payout} {MONEY_BAG}")
            saldo += payout
        else:
            tocarSom("perdeu.mp3")  # Som de derrota
            print("Não foi desta vez que você conseguiu...", sleep(2), "mas continue tentando")
            print("❌ Nada feito. Tente novamente! ❌")
            saldo -= bet

        if saldo <= 0:
            tocarSom("perdeu.mp3")  # Som de derrota
            print("😢 Você ficou sem dinheiro! O jogo acabou. Obrigado por jogar Keno! 🎱")
            sys.exit()

        input("\nPressione Enter para continuar...\n")
        return saldo

def main():
    global saldo  # Permite modificar a variável global dentro da função

    while True:
        try:
            print("\n🎲 Bem-vindo ao Cassino! 🎲")
            print(f"Seu saldo atual é de R$ {saldo}.")  # Mostra o saldo atualizado
            print("\nEscolha um jogo:")
            print("1. Blackjack")
            print("2. Slots")
            print("3. Keno")
            print("4. Sair")
            escolha = input("> ")

            if escolha == "1":
                saldo = blackjack(saldo)  # Passa o saldo para a função
            elif escolha == "2":
                saldo = slots(saldo)
            elif escolha == "3":
                saldo = keno(saldo)
            elif escolha == "4":
                print("Obrigado por jogar! 🎲")
                sys.exit()
            else:
                print("Escolha inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("\nObrigado por jogar! 🎲")
            sys.exit()

if __name__ == "__main__":
    main()
