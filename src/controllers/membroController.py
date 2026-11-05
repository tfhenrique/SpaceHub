from src.services.membroService import MembroService
from src.controllers.utilizadorController import UtilizadorController

class MembroController:
    
    def __init__(self):
        # Instancia o Service para aplicar a lógica
        self.service = MembroService()
        self.utilizador_controller = UtilizadorController() # utilizado para autenticar o membro e o utilizador

    def registar_membro(self, id_utilizador: int, nome: str, empresa: str, nif: str, email: str, telefone: str, daInicio: str, daFim: str) -> bool:
        try:
            # Verifica se os campos obrigatórios não estão vazios
            if not nome or not empresa or not nif or not email or not telefone or not daInicio or not daFim:
                print("Erro: Todos os campos obrigatórios devem ser preenchidos.")
                return False

            # Envia os dados para o Service tratar da lógica
            # nome, empresa, nif, email, telefone, plano_id, daInicio, daFim, ativo
            sucesso = self.service.registar_membro(nome, empresa, nif, email, telefone, 0, daInicio, daFim, True)
            if sucesso:
                # Obtém o ID do membro recém-criado
                id_membro = self.service.get_membro_id(nif)
                # Conecta a chave estrangeira do utilizador com a chave primária do membro recém-criado
                self.service.conectar_idMembro(id_utilizador, id_membro)
            return sucesso
        except Exception as e:
            print(f"Erro no controller de registo de membro: {e}")
            return False

    def autenticar_membro(self, id_utilizador: int) -> bool:
        try:
            # Verifica se o utilizador tem um membro associado
            utilizador_info = self.utilizador_controller.get_utilizador_info(id_utilizador)
            if not utilizador_info or not utilizador_info[1]:
                print("Nenhum membro associado a este utilizador.")
                return False

            print("Autenticação de membro bem-sucedida.")
            return True
        except Exception as e:
            print(f"Erro no controller de autenticação de membro: {e}")
            return False