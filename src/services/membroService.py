from src.repositories.membroRepository import MembroRepository

class MembroService:

    def __init__(self):
        self.repository = MembroRepository()

    def registar_membro(self, nome: str, empresa: str, nif: str, email: str, telefone: str, plano_id: int, daInicio: str, daFim: str, ativo: bool) -> bool:
        # Verifica se já existe um membro com este NIF
        membro_existente = self.repository.get_nif(nif)
        if membro_existente:
            print("\n[Aviso] Já existe um membro com este NIF.")
            return False

        # Se não existir, manda o repository inserir na base de dados
        return self.repository.inserir(nome, empresa, nif, email, telefone, plano_id, daInicio, daFim, ativo)

    def get_membro_id(self, nif: str) -> int:
        membro = self.repository.get_nif(nif)
        if membro:
            return membro[0]
        else:
            print("\n[Aviso] Membro não encontrado para o NIF fornecido.")
            return None

    def conectar_idMembro(self, id_utilizador: int, id_membro: int):
        return self.repository.conectar_idMembro(id_utilizador, id_membro)