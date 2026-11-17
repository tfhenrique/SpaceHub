from src.services.membroService import MembroService
from src.controllers.utilizadorController import UtilizadorController
from src.models.membro import Membro


class MembroController:

    def __init__(self):
        self.service = MembroService()
        self.utilizador_controller = UtilizadorController()

    def registar_membro(
        self, id_utilizador: int, nome: str, empresa: str,
        nif: str, email: str, telemovel: str
    ) -> bool:
        try:
            if not all([nome, empresa, nif, email, telemovel]):
                print("Aviso: Todos os campos obrigatórios devem ser preenchidos.")
                return False

            if len(nif) != 9 or not nif.isdigit():
                print("Aviso: NIF inválido.")
                return False

            if len(telemovel) != 9 or not telemovel.isdigit():
                print("Aviso: Número de telemóvel inválido.")
                return False

            sucesso = self.service.registar_membro(
                nome, empresa, nif, email, telemovel
            )

            if sucesso:
                id_membro = self.service.get_membro_id(nif)
                if not id_membro:
                    return False
                return self.service.conectar_idMembro(id_utilizador, id_membro)

            return False

        except Exception as erro:
            print(f"Erro no MembroController, registar_membro: {erro}")
            return False

    def atualizar_membro(
        self, id_membro: int, nome: str, empresa: str,
        nif: str, email: str, telemovel: str
    ) -> bool:
        try:
            if not all([nome, empresa, nif, email, telemovel]):
                print("Aviso: Todos os campos obrigatórios devem ser preenchidos.")
                return False

            if len(nif) != 9 or not nif.isdigit():
                print("Aviso: NIF inválido.")
                return False

            if len(telemovel) != 9 or not telemovel.isdigit():
                print("Aviso: Número de telemóvel inválido.")
                return False

            return self.service.atualizar_membro(
                id_membro, nome, empresa, nif, email, telemovel
            )

        except Exception as erro:
            print(f"Erro no MembroController, atualizar_membro: {erro}")
            return False

    def autenticar_membro(self, id_utilizador: int) -> bool:
        try:
            utilizador_info = self.utilizador_controller.get_utilizador_info(
                id_utilizador
            )
            if not utilizador_info or not utilizador_info[1]:
                print("Aviso: Nenhum membro associado a este utilizador.")
                return False

            print("Autenticação de membro bem-sucedida.")
            return True
        except Exception as erro:
            print(f"Erro no MembroController, autenticar_membro: {erro}")
            return False

    def get_member_info(self, id_membro: int) -> Membro:
        try:
            return self.service.get_member_info(id_membro)
        except Exception as erro:
            print(f"Erro no MembroController, get_member_info: {erro}")
            return None

    def mostrar_membros(self) -> list:
        try:
            return self.service.listar_membros()
        except Exception as erro:
            print(f"Erro no Controller ao listar membros: {erro}")
            return []