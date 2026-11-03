from typing import Tuple
from src.services.utilizadorService import UtilizadorService


class UtilizadorController:

    def __init__(self):
        # Instancia o Service para aplicar a lógica
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

    def get_utilizador_id(self, login: str, passhash: str) -> int:
        try:
            # Verifica se os campos não estão vazios
            if not login or not passhash:
                print("Erro: O login e a password não podem estar vazios.")
                return -1

            # Envia para o Service obter o ID do utilizador
            utilizador_id = self.service.get_utilizador_id(login, passhash)
            return utilizador_id
        except Exception as e:
            print(f"Erro no controller ao obter ID do utilizador: {e}")
            return -1

    def get_utilizador_info(self, id: int) -> Tuple[int, int, str, str, str,bool]:
        try:
            # Verifica se o ID é válido
            if id < 0:
                print("Erro: ID de utilizador inválido.")
                return None

            # Envia para o Service obter as informações do utilizador
            utilizador_info = self.service.get_utilizador_info(id)
            return utilizador_info
        except Exception as e:
            print(f"Erro no controller ao obter informações do utilizador: {e}")
            return None