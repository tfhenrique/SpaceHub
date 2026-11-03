import sys
from src.controllers.utilizadorController import UtilizadorController
from src.views.utilizadorView import UtilizadorView
from src.controllers.membroController import MembroController

class MembroView:
    def __init__(self, membro_controller):
        self.utilizador_view = UtilizadorView() # Instancia a view do utilizador para poder limpar a tela
        self.utilizador_controller = UtilizadorController()

    def membro_menu(self, utilizador_id):
        # carrega as informações do user
        utilizador_info = self.utilizador_controller.get_utilizador_info(utilizador_id)
        print(
            "Bem-vindo ", utilizador_info[2], "!\n"
            "--- Menu de Registo de Membro ---\n"
            "1 - Registar Membro\n"
            "2 - Eliminar Conta\n"
            "3 - Deslogar\n"
            "0 - Sair")
        return input("Escolha uma opção: ").strip()

    def registar_membro_menu(self, utilizador_id) -> int:
        while True:
            self.utilizador_view.limpar_tela()
            opcao = self.membro_menu(utilizador_id)

            match opcao:
                case "1":
                    print("\n--- Registo de Membro ---")
                    nome = input("Nome do Membro: ")
                    empresa = input("Empresa do Membro: ")
                    nif = input("NIF do Membro: ")
                    email = input("Email do Membro: ")
                    telefone = input("Telefone do Membro: ")
                    plano_id = None
                    daInicio = input("Data de Início (YYYY-MM-DD): ")
                    daFim = input("Data de Fim (YYYY-MM-DD): ")
                    ativo = True

                    input("\nPressiona Enter para voltar ao menu...")

                case "2":
                    print("\n--- Eliminar Conta ---")
                    confirmacao = input("Tem a certeza que deseja eliminar a sua conta? (s/n): ")
                    if confirmacao.lower() == "s":
                        #self.utilizador_controller.eliminar_conta(utilizador_id)
                        print("\nConta eliminada com sucesso!")
                    input("\nPressiona Enter para voltar ao menu...")

                case "3":
                    print("\nA deslogar...")
                    return -2

                case "0":
                    print("\nA encerrar o programa...")
                    sys.exit()

                case _:
                    print("\nOpção inválida! Tente novamente.")
                    input("\nPressiona Enter para voltar ao menu...")