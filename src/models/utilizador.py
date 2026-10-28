class Utilizador:
    def __init__(self, idUtilizador: int, login: str, passhash: str, perfil: str = "Indefinido", ativo: bool = True):
        self.idUtilizador = idUtilizador
        self.login = login
        self.passhash = passhash
        self.perfil = perfil
        self.ativo = ativo

    def __str__(self):
        return f"Utilizador(ID: {self.idUtilizador}, Login: {self.login}, Perfil: {self.perfil}, Ativo: {self.ativo})"