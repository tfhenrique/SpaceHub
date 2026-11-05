import time
from src.controllers.membroController import MembroController
from src.views.utilizadorView import UtilizadorView


class MembroView:

    def __init__(self):
        self.uti_view = UtilizadorView()  # Instancia da UtilizadorView para poder usar limpar_tela()
        self.membro_controller = MembroController()

    def menu_membro(self, membro_nome) -> str:
        self.uti_view.limpar_tela()
        print(
            "-" * 6, " Menu Membro ", 6 * "-",
            f"Bem-vindo, {membro_nome}!\n",
            "1 - Atualizar Informações",
            "2 - Ver Detalhes / Listar",
            "0 - Voltar / Terminar Sessão"
        )
        return input("Escolha uma opção: ").strip()

    def fluxo_membro(self, utilizador_id):
        # Verifica se o utilizador já tem perfil de membro criado
        membro_info = self.membro_controller.get_member_info(utilizador_id)

        while True:
            if not membro_info:
                # Se ainda não for membro, obriga/oferece a criação do perfil de membro
                self.utilizador_view.limpar_tela()
                print(
                    "\nAinda não tem um perfil de Membro associado à sua conta de"
                    " Utilizador."
                )
                opcao = input("Deseja registar-se como Membro agora? (s/n): ")
                if opcao.lower() == "s":
                    self.registar_membro_form(utilizador_id)
                    membro_info = self.membro_controller.get_member_info(utilizador_id)  # Atualiza
                else:
                    break  # Volta ao menu anterior se não quiser
            else:
                # Se já é membro, mostra o menu exclusivo de membro
                opcao = self.menu_membro(membro_info.nome)

                match opcao:
                    case "1":
                        print("\n[Funcionalidade de Atualizar em desenvolvimento...]")
                        input("Pressiona Enter para continuar...")
                    case "2":
                        print(f"\nEmpresa: {membro_info.empresa} | NIF: {membro_info.NIF}")
                        input("Pressiona Enter para continuar...")
                    case "0":
                        break  # Sai do menu de membro e volta ao login/menu principal
                    case _:
                        print("\nOpção inválida!")
                        time.sleep(1)

    def registar_membro_form(self, utilizador_id):
        self.utilizador_view.limpar_tela()
        print("\n--- Registo de Membro ---")
        nome = input("Nome: ")
        empresa = input("Empresa: ")
        nif = input("NIF: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        daInicio = input("Data de Início (YYYY-MM-DD): ")
        daFim = input("Data de Fim (YYYY-MM-DD): ")

        sucesso = self.membro_controller.registar_membro(
            utilizador_id, nome, empresa, nif, email, telefone, daInicio, daFim
        )
        if sucesso:
            print(f"\nMembro '{nome}' registado com sucesso!")
        else:
            print(f"\nFalha ao registar o membro.")
            input("\nPressiona Enter para continuar...")