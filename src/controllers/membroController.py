from src.services.membroService import MembroService

class MembroController:
    
    def __init__(self):
        # Instancia o Service para aplicar a lógica
        self.service = MembroService()

    def registar_membro(self, nome: str, empresa: str, nif: str, email: str, telefone: str, daInicio: str, daFim: str) -> bool:
        try:
            # Verifica se os campos obrigatórios não estão vazios
            if not nome or not empresa or not nif or not email or not telefone or not daInicio or not daFim:
                print("Erro: Todos os campos obrigatórios devem ser preenchidos.")
                return False

            # Envia os dados para o Service tratar da lógica
            # nome, empresa, nif, email, telefone, plano_id, daInicio, daFim, ativo
            sucesso = self.service.registar_membro(nome, empresa, nif, email, telefone, 0, daInicio, daFim, True)
            return sucesso
        except Exception as e:
            print(f"Erro no controller de registo de membro: {e}")
            return False