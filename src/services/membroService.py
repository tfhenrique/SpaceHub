from src.repositories.membroRepository import MembroRepository

class MembroService:

    def __init__(self):
        self.repository = MembroRepository()

    def registar_membro(self, nome: str, empresa: str, nif: str, email: str, telefone: str, plano_id: int, daInicio: str, daFim: str, ativo: bool) -> bool:
        # Verifica se já existe um membro com este NIF
        membro_existente = self.repository.buscar_por_nif(nif)
        if membro_existente:
            print("\n[Aviso] Já existe um membro com este NIF.")
            return False

        # Se não existir, manda o repository inserir na base de dados
        return self.repository.inserir(nome, empresa, nif, email, telefone, plano_id, daInicio, daFim, ativo)