import pyodbc
from db.connection import DB_CONFIG
from src.models.utilizador import Utilizador


class UtilizadorRepository:

    def __init__(self):
        self.db_config = DB_CONFIG

    def inserir(self, utilizador: Utilizador) -> bool:
        try:
            conn = pyodbc.connect(self.db_config)
            cursor = conn.cursor()

            # Como o utilizador ainda não se cadastrou como membro, o membro_id é None
            cursor.execute(
                """
                INSERT INTO Utilizador (membro_id, login_utilizador, password_hash, perfil, ativo) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (utilizador.membro_id, utilizador.login, utilizador.password_hash, utilizador.perfil, 1),
            )

            conn.commit()
            conn.close()
            return True
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no uti repository inserir: {e}\033[0m")
            return False

    def buscar_por_login(self, login: str) -> Utilizador | None:
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT idUtilizador, membro_id, login_utilizador, password_hash, perfil, ativo 
                FROM Utilizador 
                WHERE login_utilizador = ?
                """,
                (login,),
            )
            row = cursor.fetchone()
            conexao.close()

            if row:
                # Mapeia o resultado do SQL diretamente para a nossa classe Utilizador
                return Utilizador(
                    id=row[0],
                    membro_id=row[1],
                    login=row[2],
                    password_hash=row[3],
                    perfil=row[4],
                    ativo=row[5],
                )
            return None
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no uti repository no buscar_por_login: {e}\033[0m")
            return None

    def buscar_por_id(self, id_utilizador: int) -> Utilizador | None:
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                        SELECT idUtilizador, membro_id, login_utilizador, password_hash, perfil, ativo 
                        FROM Utilizador 
                        WHERE idUtilizador = ?
                        """,
                (id_utilizador,),
            )
            row = cursor.fetchone()
            conexao.close()

            if row:
                return Utilizador(
                    id=row[0],
                    membro_id=row[1],
                    login=row[2],
                    password_hash=row[3],
                    perfil=row[4],
                    ativo=row[5],
                )
            return None
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no uti repository no buscar_por_id: {e}\033[0m")
            return None