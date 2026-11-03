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