from controllers.casino_controller import CasinoController

def main():
    """
    O Ponto de Entrada. Cara, agora o main tá magrinho, 
    tipo eu depois de uma dieta de sanduíche de alface.
    O trabalho pesado tá todo no Controller agora.
    """
    app = CasinoController()
    app.run()

if __name__ == "__main__":
    main()
