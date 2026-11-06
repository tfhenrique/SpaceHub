class Utilizador:

    def __init__(self, id=None, membro_id=None, login=None, password_hash=None, perfil="USER", ativo=True):
        self.id = id
        self.membro_id = membro_id
        self.login = login
        self.password_hash = password_hash
        self.perfil = perfil
        self.ativo = ativo