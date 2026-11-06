from src.services.membroService import MembroService
from src.controllers.utilizadorController import UtilizadorController

from src.models.membro import Membro

class MembroController:
    
    def __init__(self):
        self.service = MembroService()
        self.utilizador_controller = UtilizadorController()

    def registar_membro(self, id_utilizador: int, nome: str, empresa: str, nif: str, email: str, telemovel: str) -> bool:
        try:
            # Verifica se os campos obrigatórios não estão vazios
            if not nome or not empresa or not nif or not email or not telemovel:
                print("\033[93mAviso: Todos os campos obrigatórios devem ser preenchidos.\033[0m")
                return False
            elif len(nif) != 9:
                print("\033[93mAviso: NIF inválido\033[0m")
                return False
            elif len(telemovel) != 9:
                print("\033[93mAviso: número de telemovel inválido\033[0m")
                return False
            # Envia os dados para o Service
            sucesso = self.service.registar_membro(nome, empresa, nif, email, telemovel)
            if sucesso:
                # Obtém o ID do membro recém-criado
                id_membro = self.service.get_membro_id(nif)
                # Conecta a chave estrangeira do utilizador com a chave primária do membro recém-criado
                self.service.conectar_idMembro(id_utilizador, id_membro)
            return sucesso
        except Exception as e:
            print(f"\033[91mErro no membro controller, registar_membro: {e}\033[0m")
            return False

    def autenticar_membro(self, id_utilizador: int) -> bool:
        try:
            # Verifica se o utilizador tem um membro associado
            utilizador_info = self.utilizador_controller.get_utilizador_info(id_utilizador)
            if not utilizador_info or not utilizador_info[1]:
                print("\033[93mAviso: Nenhum membro associado a este utilizador.\033[0m")
                return False

            print("\033[92mAutenticação de membro bem-sucedida.\033[0m")
            return True
        except Exception as e:
            print(f"\033[91mErro no membro controller, autenticar_membro: {e}\033[0m")
            return False

    def get_member_info(self, id_membro: int) -> Membro:
        try:
            membro_info = self.service.get_member_info(id_membro)
            return membro_info
        except Exception as e:
            print(f"\033[91mErro no membro controller, get_membro_info: {e}\033[0m")
            return None

    def mostrar_membros(self) -> list:
        try:
            return self.service.listar_membros()
        except Exception as e:
            print(f"\033[91mErro no controller ao listar membros: {e}\033[0m")
            return []