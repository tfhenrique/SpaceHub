from src.repositories.utilizadorRepository import UtilizadorRepository


class UtilizadorService:

    def __init__(self):
        self.repository = UtilizadorRepository()

    def registar_utilizador(self, login: str, passhash: str) -> bool:
        # Verificar se já existe um utilizador com este login
        utilizador_existente = self.repository.buscar_por_login(login)
        if utilizador_existente:
            print("\n[Aviso] Já existe um utilizador com este nome.")
            return False

        # Se não existir, manda o repository inserir na base de dados
        return self.repository.inserir(login, passhash)

    def autenticar(self, login: str, passhash: str) -> bool:
        # Vai buscar o utilizador à base de dados para comparar os dados
        utilizador = self.repository.buscar_por_login(login)
        
        if not utilizador:
            return False
        # A posição do password no tuple devolvido pelo fetchone() realizado pelo repository
        password_na_bd = utilizador[3] 

        if password_na_bd == passhash:
            return True
        
        return False