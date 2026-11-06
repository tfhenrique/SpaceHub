from src.repositories.membroRepository import MembroRepository
from src.models.membro import Membro

class MembroService:

    def __init__(self):
        self.repository = MembroRepository()

    def registar_membro(self, nome: str, empresa: str, nif: str, email: str, telemovel: str) -> bool:
        # Verifica se já existe um membro com este NIF
        membro_existente = self.repository.get_nif(nif)
        if membro_existente:
            print("\n\033[93mAviso: Já existe um membro com este NIF.\033[0m")
            return False

        membro = Membro(nome=nome, empresa=empresa, nif=nif, email=email, telemovel=telemovel)

        # Se não existir, manda o repository inserir na base de dados
        return self.repository.inserir(membro)

    def get_membro_id(self, nif: str) -> int:
        membro = self.repository.get_nif(nif)
        if membro:
            return membro.id
        else:
            print("\n\033[93mAviso: Membro não encontrado para o NIF fornecido.\033[0m")
            return None

    def conectar_idMembro(self, id_utilizador: int, id_membro: int):
        return self.repository.conectar_idMembro(id_utilizador, id_membro)

    def get_member_info(self, idMembro: int) -> Membro:
        membro_info = self.repository.get_member_info(idMembro)
        return membro_info

    def listar_membros(self) -> list:
        return self.repository.get_Membros()