from src.models.utilizador import Utilizador
from src.repositories.utilizadorRepository import UtilizadorRepository


class UtilizadorService:

    def __init__(self):
        self.repository = UtilizadorRepository()

    def registar_utilizador(self, login: str, passhash: str) -> bool:
        # Verificar se já existe um utilizador com este login
        utilizador_existente = self.repository.buscar_por_login(login)
        if utilizador_existente:
            print("\n\033[93mAviso: Já existe um utilizador com este nome.\033[0m")
            return False

        # Cria o objeto Utilizador para enviar para o repository
        novo_utilizador = Utilizador(login=login, password_hash=passhash)

        # Envia o objeto model para o repository inserir na base de dados
        return self.repository.inserir(novo_utilizador)

    def autenticar(self, login: str, passhash: str) -> bool:
        # Vai buscar o objeto utilizador à base de dados
        utilizador = self.repository.buscar_por_login(login)

        if not utilizador:
            return False

        # Compara a password usando a propriedade limpa do objeto
        if utilizador.password_hash == passhash:
            return True

        return False

    def get_utilizador_id(self, login: str) -> int:
        # Vai buscar o utilizador à base de dados apenas com o login
        utilizador = self.repository.buscar_por_login(login)

        if not utilizador:
            return -1

        # Retorna o ID armazenado no objeto
        return utilizador.id

    def get_utilizador_info(self, id: int) -> Utilizador | None:
        # Retorna diretamente o objeto Utilizador encontrado pelo ID
        return self.repository.buscar_por_id(id)