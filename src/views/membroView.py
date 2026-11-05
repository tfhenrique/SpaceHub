import sys
import time
from src.controllers.utilizadorController import UtilizadorController
from src.views.utilizadorView import UtilizadorView
from src.controllers.membroController import MembroController

class MembroView:
    def __init__(self):
        self.utilizador_view = UtilizadorView() # Instancia a view do utilizador para poder limpar a tela
        self.utilizador_controller = UtilizadorController()
        self.membro_controller = MembroController()

    def membro_menu(self, utilizador_id):
        self.utilizador_view.limpar_tela()
        # carrega as informações do user
        utilizador_info = self.utilizador_controller.get_utilizador_info(utilizador_id)
        print(
            "Bem-vindo ", utilizador_info[2], "!\n"
            "--- Menu de Registo de Membro ---\n"
            "1 - Registar Membro\n"
            "2 - Logar Membro\n"
            "3 - Eliminar Conta\n"
            "4 - Deslogar\n"
            "0 - Sair")
        return input("Escolha uma opção: ").strip()

    def registar_membro_menu(self, utilizador_id) -> int:
        submenu = False
        while True:
            self.utilizador_view.limpar_tela()
            if not submenu:
                opcao = self.membro_menu(utilizador_id)
                match opcao:
                    case "1":
                        self.utilizador_view.limpar_tela()
                        print("\n--- Registo de Membro ---")
                        nome = input("Nome: ")
                        empresa = input("Empresa: ")
                        nif = input("NIF: ")
                        email = input("Email: ")
                        telefone = input("Telefone: ")
                        daInicio = input("Data de Início (YYYY-MM-DD): ")
                        daFim = input("Data de Fim (YYYY-MM-DD): ")

                        sucesso = self.membro_controller.registar_membro(utilizador_id, nome, empresa, nif, email, telefone, daInicio, daFim)
                        if sucesso:
                            print(f"\nMembro '{nome}' registado com sucesso!")
                        else:
                            print(f"\nFalha ao registar o membro '{nome}'.")

                        input("\nPressiona Enter para voltar ao menu...")

                    case "2":
                        sucesso = self.membro_controller.autenticar_membro(utilizador_id)
                        if sucesso:
                            submenu = True

                    case "3":
                        self.utilizador_view.limpar_tela()
                        print("\n--- Eliminar Conta ---")
                        confirmacao = input("Tem a certeza que deseja eliminar a sua conta? (s/n): ").strip().lower()
                        if confirmacao == 's':
                            sucesso = self.utilizador_controller.eliminar_utilizador(utilizador_id)
                            if sucesso:
                                print("\nConta eliminada com sucesso. A encerrar o programa...")
                                time.sleep(2)
                                sys.exit()
                            else:
                                print("\nFalha ao eliminar a conta.")
                                input("\nPressiona Enter para voltar ao menu...")
                        else:
                            print("\nOperação cancelada.")
                            input("\nPressiona Enter para voltar ao menu...")

                    case "4":
                        print("\nA deslogar...")
                        time.sleep(1)
                        return -2  # Indica que o utilizador deslogou

                    case "0":
                        print("\nA encerrar o programa...")
                        time.sleep(1)
                        sys.exit()

                    case _:
                        print("\nOpção inválida! Tente novamente.")
            else:
                print("\nSubmenu ainda não implementado.")
                input("\nPressiona Enter para voltar ao menu...")