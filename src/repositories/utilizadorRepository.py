import pyodbc
from db.connection import DB_CONFIG
from src.models.utilizador import Utilizador

class UtilizadorRepository:

    def __init__(self, db_path="db/SpaceHub.db"):
        self.db_config = DB_CONFIG

    def inserir(self, utilizador: Utilizador) -> bool:
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()
            
            # Como o utilizador ainda não se codrastrou como membro o membro_id é None
            cursor.execute(
                """
                INSERT INTO Utilizador (membro_id, login_utilizador, password_hash, perfil, ativo) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (None, utilizador.login, utilizador.password_hash, "USER", 1),
            )

            conexao.commit()
            conexao.close()
            return True
        except pyodbc.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return False

    def buscar_por_login(self, login: str):
        try:
            conexao = pyodbc.connect(self.db_config)
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
        except pyodbc.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return None

    def buscar_por_id(self, login: int, passhash: str):
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT * 
                FROM Utilizador 
                WHERE login_utilizador = ? AND password_hash = ?
                """
                , (login, passhash)
            )
            resultado = cursor.fetchone()

            conexao.close()
            return resultado
        except pyodbc.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return None