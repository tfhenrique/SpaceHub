class Utilizador:

    def __init__(self, login, perfil, membro_id=None, ativo=True, password_hash=None, id=None):
        self.id = id
        self.membro_id = membro_id
        self.login = login
        self.password_hash = password_hash
        self.perfil = perfil
        self.ativo = ativo