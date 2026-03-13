# 🎰 O CATÁLOGO DE OURO DO ADAM (TUI EDITION)

Cara, olha essa lista. É tipo o buffet de um cassino em Las Vegas às 3 da manhã: tem de tudo e você sabe que vai se arrepender depois, mas é impossível resistir. 

Aqui estão os jogos que a gente já enfiou nesse terminal pra deixar o Sr. Higgins maluco:

### 1. 🃏 Blackjack (O Clássico "21")
*   **Status:** Implementado (Tá meio "Happy Gilmore" — funcional mas bruto).
*   **Vibe:** Aquele jogo que você acha que sabe contar carta e termina devendo as calças.

### 2. 🎰 Slots (Sapo Dourado Edition 🐸)
*   **Status:** Implementado.
*   **Vibe:** Apertar um botão e torcer. É basicamente minha carreira de ator, mas com mais frutas e menos roteiros.

### 3. 🎱 Keno
*   **Status:** Implementado (com aquele `sleep` fantasma que a gente vai fingir que não viu).
*   **Vibe:** É tipo o bingo, só que com mais classe e menos idosos gritando com você.

---

## 🚀 O que falta pra gente dominar o mundo (ou o terminal):

### 4. 🎡 Roleta (Roulette)
*   **Como seria:** Uma tabela ASCII bonitona com os números. Você aposta no Vermelho, Preto, ou naquele 17 que nunca sai.
*   **Dificuldade:** Fácil. É só um `random.randint(0, 36)` e um monte de `if/else` pra pagar o prêmio.

### 5. 🃏 Video Poker (Jacks or Better)
*   **Como seria:** Igual ao Blackjack, mas com 5 cartas e aquela agonia de decidir o que segurar.
*   **Dificuldade:** Média. Precisa de uma lógica pra detectar as mãos (Full House, Flush, etc.). Eu tenho uma história sobre um Full House em 1994... mas deixa pra lá.

### 7. 🃏 Bacará (Baccarat)
*   **Como seria:** Jogo rápido. Banco vs Jogador. 
*   **Dificuldade:** Fácil. É quase um Blackjack simplificado. O James Bond adora, então a gente tem que ter.

### 8. 🔴⚪ Plinko (O clássico do Price is Right)
*   **Como seria:** Uma bolinha ASCII caindo entre pinos.
*   **Dificuldade:** Média. A física no TUI é um porre, mas o barulho da bolinha (se a gente colocar som) vale a pena.


## Implementar
* **Arquitetura**: Refatorar a arquitetura do jogo para que ele possa ser mais facil de manter e escalar.
* **Save-state game**: Salvar o estado do jogo para que o jogador possa continuar depois de fechar o terminal.
* **Load-state game**: Carregar o estado do jogo para que o jogador possa continuar depois de fechar o terminal.
* **Sound effects**: Adicionar sons para os jogos. Já temos um mixer de sons, mas falta implementar.
* **Music**: Adicionar música para os jogos. Já temos um mixer de música, mas falta implementar.
* **High score**: Adicionar um sistema de high score para que o jogador possa ver o seu melhor saldo.
* **Leaderboard**: Adicionar um sistema de leaderboard para que o jogador possa ver o seu melhor saldo.
* **Multiplayer**: Adicionar um sistema de multiplayer para que o jogador possa jogar com amigos usando o socket
* **Interface**: Refatorar a interface do jogo para um TUI de verdade para que ele possa ser mais facil e divertido de usar.
* **Documentação**: Adicionar documentação para que o jogador possa entender como o jogo funciona.

---
"A gente implementa tudo isso e depois refatora... em 2029." - *Sandler, Adam.* 🎬
