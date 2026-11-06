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
            "-" * 6, " Menu Membro ", 6 * "-", "\n"
            f"Bem-vindo, {membro_nome}!\n",
            "1 - Atualizar Informações\n",
            "2 - Ver Detalhes / Listar\n",
            "3 - Listar todos os Membros (apenas para avalição)\n",
            "0 - Voltar / Terminar Sessão"
        )
        return input("Escolha uma opção: ").strip()

    def fluxo_membro(self, utilizador_id):
        # Verifica se o utilizador já tem perfil de membro criado
        membro_info = self.membro_controller.get_member_info(utilizador_id)

        while True:
            if not membro_info:
                # Se ainda não for membro, obriga/oferece a criação do perfil de membro
                self.uti_view.limpar_tela()
                print("\n\033[93mAviso: Ainda não tem um perfil de Membro associado à sua conta de Utilizador.\033[0m")
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
                        print("\n\033[93mAviso: Funcionalidade de Atualizar em desenvolvimento...\033[0m")
                        input("Pressiona Enter para continuar...")
                        continue
                    case "2":
                        print(f"\nEmpresa: {membro_info.empresa} | NIF: {membro_info.nif}")
                        input("Pressiona Enter para continuar...")
                        continue
                    case "3":
                        self.mostrar_todos_membros()
                        input("Pressiona Enter para continuar...")
                        continue
                    case "0":
                        break  # Sai do menu de membro e volta ao login/menu principal
                    case _:
                        print("\n\033[93mAviso: Opção inválida!\033[0m")
                        time.sleep(1)

    def registar_membro_form(self, utilizador_id):
        self.uti_view.limpar_tela()
        print("\n--- Registo de Membro ---")
        nome = input("Nome: ")
        empresa = input("Empresa: ")
        nif = input("NIF: ")
        email = input("Email: ")
        telefone = input("Telefone: ")

        sucesso = self.membro_controller.registar_membro(utilizador_id, nome, empresa, nif, email, telefone)
        if sucesso:
            print(f"\n\033[92mMembro '{nome}' registado com sucesso!\033[0m")
            time.sleep(2)
        else:
            print(f"\n\033[93mAviso: Falha ao registar o membro.\033[0m")
            input("\nPressiona Enter para continuar...")

    def mostrar_todos_membros(self):
        # Cabeçalho da tabela formatado a azul (\033[94m)
        print("\n" + "\033[94m" + "=" * 115 + "\033[0m")
        print(
            "\033[94m"
            f"{'ID':<4} | {'Nome':<18} | {'Empresa':<12} | {'NIF':<10} |"
            f" {'Telemóvel':<10} | {'Plano':<6} | {'Início':<10} | {'Fim':<10}"
            f" | {'Ativo':<5}" + "\033[0m"
        )
        print("\033[94m" + "=" * 115 + "\033[0m")

        membros = self.membro_controller.mostrar_membros()

        if not membros:
            print(f"{'Não existem membros registados na base de dados.':^115}")
            print("=" * 115)
            return

        for m in membros:
            # Formata o booleano 'ativo' para 'Sim' ou 'Não'
            ativo_str = "Sim" if m.ativo else "Não"

            print(
                f"{str(m.id):<4} | {str(m.nome):<18} | {str(m.empresa):<12} |"
                f" {str(m.nif):<10} | {str(m.telemovel):<10} |"
                f" {str(m.plano_id):<6} | {str(m.data_inicio):<10} |"
                f" {str(m.data_fim):<10} | {ativo_str:<5}"
            )

        print("=" * 115)