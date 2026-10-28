class Utilizador:
    total_utilizadores = 0

    def __init__(self, idUtilizador: int, login: str, passhash: str, perfil: str, ativo: bool):
        self.idUtilizador = idUtilizador
        self.login = login
        self.passhash = passhash
        self.perfil = perfil
        self.ativo = ativo
        Utilizador.total_utilizadores += 1

    def criarUtilizador(self, user: Utilizador):
        pass

    def autenticar(self, login: str, passhash: str) -> str:
        return ""