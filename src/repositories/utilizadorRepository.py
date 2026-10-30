import sqlite3


class UtilizadorRepository:

    def __init__(self, db_path="db/SpaceHub.db"):
        self.db_path = db_path

    def inserir(self, login: str, passhash: str) -> bool:
        try:
            conexao = sqlite3.connect(self.db_path)
            cursor = conexao.cursor()
            
            # Como o utilizador ainda não se codrastrou como membro o membro_id é None
            cursor.execute(
                """
                INSERT INTO Utilizador (membro_id, login_utilizador, password_hash, perfil, ativo) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (None, login, passhash, "USER", 1),
            )

            conexao.commit()
            conexao.close()
            return True
        except sqlite3.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return False

    def buscar_por_login(self, login: str):
        try:
            conexao = sqlite3.connect(self.db_path)
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT * 
                FROM Utilizador 
                WHERE login_utilizador = ?
                """
                , (login,)
            )
            resultado = cursor.fetchone()

            conexao.close()
            return resultado
        except sqlite3.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return None