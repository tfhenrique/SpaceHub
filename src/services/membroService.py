from src.repositories.membroRepository import MembroRepository
from src.models.membro import Membro


class MembroService:

    def __init__(self):
        self.repository = MembroRepository()

    def registar_membro(
        self, nome: str, empresa: str, nif: str, email: str, telemovel: str
    ) -> bool:
        # Impede o registo de dois membros com o mesmo NIF.
        membro_existente = self.repository.get_nif(nif)
        if membro_existente:
            print("Aviso: Já existe um membro com este NIF.")
            return False

        membro = Membro(
            nome=nome,
            empresa=empresa,
            nif=nif,
            email=email,
            telemovel=telemovel
        )
        return self.repository.inserir(membro)

    def atualizar_membro(
        self, id_membro: int, nome: str, empresa: str,
        nif: str, email: str, telemovel: str
    ) -> bool:
        # Se o NIF pertencer a outro membro, não permite a alteração.
        membro_existente = self.repository.get_nif(nif)
        if membro_existente and membro_existente.id != id_membro:
            print("Aviso: Já existe outro membro com este NIF.")
            return False

        return self.repository.atualizar(
            id_membro, nome, empresa, nif, email, telemovel
        )

    def get_membro_id(self, nif: str) -> int:
        membro = self.repository.get_nif(nif)
        if membro:
            return membro.id

        print("Aviso: Membro não encontrado para o NIF fornecido.")
        return None

    def conectar_idMembro(self, id_utilizador: int, id_membro: int):
        return self.repository.conectar_idMembro(id_utilizador, id_membro)

    def get_member_info(self, id_membro: int) -> Membro:
        return self.repository.get_member_info(id_membro)

    def listar_membros(self) -> list:
        return self.repository.get_Membros()