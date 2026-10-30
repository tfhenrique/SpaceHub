import os
from src.controllers.utilizadorController import UtilizadorController

class UtilizadorView:
    def __init__(self):
        self.controller = UtilizadorController()

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def exibir_menu(self) -> str:
        print(
            "--- MENU PRINCIPAL ---\n"
            "1 - Criar Utilizador\n"
            "2 - Autenticar Utilizador\n"
            "0 - Sair"
        )
        return input("Escolha uma opção: ").strip()

    def menu_principal(self):
        while True:
            self.limpar_tela()
            opcao = self.exibir_menu()

            match opcao:
                case "1":
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

                case "2":
                    self.limpar_tela()
                    print("\n--- Autenticação ---")
                    login = input("Nome de utilizador: ")
                    passhash = input("Password: ")

                    sucesso = self.controller.autenticar_utilizador(login, passhash)
                    if sucesso:
                        print(f"\nAutenticação efetuada com sucesso para '{login}'.")
                    else:
                        print(f"\nFalha ao autenticar o utilizador '{login}'.")

                    input("\nPressiona Enter para voltar ao menu...")

                case "0":
                    print("\nA encerrar o programa...")
                    break

                case _:
                    print("\nOpção inválida! Tente novamente.")
                    input("\nPressiona Enter para continuar...")
