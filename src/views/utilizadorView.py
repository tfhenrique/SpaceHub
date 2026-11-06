import os, subprocess
import sys
import time
from src.controllers.utilizadorController import UtilizadorController


class UtilizadorView:

    def __init__(self):
        self.controller = UtilizadorController()

    def limpar_tela(self):
        subprocess.run(["cls" if os.name == "nt" else "clear"], shell=True)

    def exibir_menu(self) -> str:
        print(
            "-" * 6, " Bem vindo a SpaceHub v1.01 ", 6 * "-", "\n",
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
                        print(f"\n\033[92mUtilizador '{login}' registado com sucesso!\033[0m")
                    else:
                        print(f"\n\033[93mAviso: Falha ao registar o utilizador '{login}'.\033[0m")

                    input("\nPressiona Enter para voltar ao menu...")

                case "2":  # Autentica e devolve o ID para o main.py
                    self.limpar_tela()
                    print("\n--- Autenticação ---")
                    login = input("Nome de utilizador: ")
                    passhash = input("Password: ")

                    sucesso = self.controller.autenticar_utilizador(login, passhash)
                    if sucesso:
                        print(f"\n\033[92mAutenticação efetuada com sucesso para '{login}'.\033[0m")
                        time.sleep(1)  # Pequena pausa fluida antes de entrar no menu seguinte
                        return self.controller.get_utilizador_id(login)
                    else:
                        print(f"\n\033[93mAviso: Falha ao autenticar o utilizador '{login}'.\033[0m")
                        input("\nPressiona Enter para voltar ao menu...")

                case "0":  # Sai do programa
                    print("\033[96m\nA encerrar o programa...\033[0m")
                    time.sleep(1)
                    sys.exit()

                case _:  # Opção inválida
                    self.limpar_tela()
                    print("\n\033[93mAviso: Opção inválida! Tente novamente.\033[0m")
                    input("\nPressiona Enter para voltar ao menu...")