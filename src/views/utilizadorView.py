import os
import sys
import time
from src.controllers.utilizadorController import UtilizadorController


class UtilizadorView:

    def __init__(self):
        self.controller = UtilizadorController()

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def exibir_menu(self) -> str:
        print(
            "-" * 6, " Bem vindo a SpaceHub 0.1 ", 6 * "-", "\n",
            "1 - Criar Utilizador\n",
            "2 - Autenticar Utilizador\n",
            "0 - Sair"
        )
        return input("Escolha uma opção: ").strip()

    def menu_principal(self) -> int:
        while True:
            self.limpar_tela()
            opcao = self.exibir_menu()

            match opcao:
                case "1":  # Cria um utilizador
                    self.limpar_tela()
                    print("\n--- Criar Utilizador ---")
                    login = input("Nome de utilizador: ")
                    passhash = input("Password: ")

                    sucesso = self.controller.registar_utilizador(login, passhash)

                    if sucesso:
                        print(f"\nUtilizador '{login}' registado com sucesso!")
                    else:
                        print(f"\nFalha ao registar o utilizador '{login}'.")

                    input("\nPressiona Enter para voltar ao menu...")

                case "2":  # Autentica e devolve o ID para o main.py
                    self.limpar_tela()
                    print("\n--- Autenticação ---")
                    login = input("Nome de utilizador: ")
                    passhash = input("Password: ")

                    sucesso = self.controller.autenticar_utilizador(login, passhash)
                    if sucesso:
                        print(f"\nAutenticação efetuada com sucesso para '{login}'.")
                        time.sleep(1)  # Pequena pausa fluida antes de entrar no menu seguinte
                        return self.controller.get_utilizador_id(login)
                    else:
                        print(f"\nFalha ao autenticar o utilizador '{login}'.")
                        input("\nPressiona Enter para voltar ao menu...")

                case "0":  # Sai do programa
                    print("\nA encerrar o programa...")
                    time.sleep(1)
                    sys.exit()

                case _:  # Opção inválida
                    print("\nOpção inválida! Tente novamente.")
                    input("\nPressiona Enter para voltar ao menu...")