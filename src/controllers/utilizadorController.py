from src.models.utilizador import Utilizador
from src.services.utilizadorService import UtilizadorService


class UtilizadorController:

    def __init__(self):
        self.service = UtilizadorService()

    def registar_utilizador(self, login: str, passhash: str) -> bool:
        try:
            # Verifica se os campos não estão vazios
            if not login or not passhash:
                print("Erro: O login e a password não podem estar vazios.")
                return False

            # Envia os dados para o Service tratar da lógica
            sucesso = self.service.registar_utilizador(login, passhash)
            return sucesso
        except Exception as e:
            print(f"Erro no controller de registo: {e}")
            return False

    def autenticar_utilizador(self, login: str, passhash: str) -> bool:
        try:
            # Verifica se os campos não estão vazios
            if not login or not passhash:
                print("Erro: O login e a password não podem estar vazios.")
                return False

            # Envia para o Service verificar a autenticação
            sucesso = self.service.autenticar(login, passhash)
            return sucesso
        except Exception as e:
            print(f"Erro no controller de autenticação: {e}")
            return False

    def get_utilizador_id(self, login: str) -> int:
        try:
            # Verifica se o campo não está vazio
            if not login:
                print("Erro: O login não pode estar vazio.")
                return -1

            # Envia para o Service obter o ID do utilizador apenas com base no login
            utilizador_id = self.service.get_utilizador_id(login)
            return utilizador_id
        except Exception as e:
            print(f"Erro no controller ao obter ID do utilizador: {e}")
            return -1

    def get_utilizador_info(self, id: int) -> Utilizador:
        try:
            # Verifica se o ID é válido (geralmente IDs em bases de dados começam em 1, mas 0 ou positivo serve)
            if id is None or id < 0:
                print("Erro: ID de utilizador inválido.")
                return None

            # Envia para o Service obter as informações do utilizador
            utilizador_info = self.service.get_utilizador_info(id)
            return utilizador_info
        except Exception as e:
            print(f"Erro no controller ao obter informações do utilizador: {e}")
            return None