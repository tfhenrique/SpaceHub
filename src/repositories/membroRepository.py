import pyodbc

from db.connection import DB_CONFIG
from src.models.membro import Membro


class MembroRepository:

    def __init__(self, db_path="db/SpaceHub.db"):
        self.db_config = DB_CONFIG

    def inserir(self, membro: Membro) -> bool:
        conexao = None
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO Membro
                    (nome, empresa, NIF, email, telemovel, plano_id,
                     data_inicio, data_fim, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    membro.nome, membro.empresa, membro.nif, membro.email,
                    membro.telemovel, membro.plano_id, membro.data_inicio,
                    membro.data_fim, membro.ativo
                )
            )

            conexao.commit()
            return True

        except pyodbc.Error as erro:
            print(f"Erro no MembroRepository, inserir: {erro}")
            return False
        finally:
            if conexao:
                conexao.close()

    def atualizar(
        self, id_membro: int, nome: str, empresa: str,
        nif: str, email: str, telemovel: str
    ) -> bool:
        conexao = None
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE Membro
                SET nome = ?, empresa = ?, NIF = ?, email = ?, telemovel = ?
                WHERE idMembro = ?
                """,
                (nome, empresa, nif, email, telemovel, id_membro)
            )

            if cursor.rowcount == 0:
                return False

            conexao.commit()
            return True

        except pyodbc.Error as erro:
            print(f"Erro no MembroRepository, atualizar: {erro}")
            return False
        finally:
            if conexao:
                conexao.close()

    def get_nif(self, nif: str) -> Membro | None:
        conexao = None
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT * FROM Membro WHERE NIF = ?",
                (nif,)
            )
            row = cursor.fetchone()

            if row:
                return Membro(
                    id=row[0], nome=row[1], empresa=row[2], nif=row[3],
                    email=row[4], telemovel=row[5], plano_id=row[6],
                    data_inicio=row[7], data_fim=row[8], ativo=row[9]
                )
            return None

        except pyodbc.Error as erro:
            print(f"Erro no MembroRepository, get_nif: {erro}")
            return None
        finally:
            if conexao:
                conexao.close()

    def conectar_idMembro(self, id_utilizador: int, id_membro: int):
        conexao = None
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE Utilizador
                SET membro_id = ?, perfil = 'MEMBER'
                WHERE idUtilizador = ?
                """,
                (id_membro, id_utilizador)
            )

            conexao.commit()
            return cursor.rowcount > 0

        except pyodbc.Error as erro:
            print(f"Erro no MembroRepository, conectar_idMembro: {erro}")
            return False
        finally:
            if conexao:
                conexao.close()

    def get_member_info(self, id_membro: int) -> Membro | None:
        conexao = None
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT * FROM Membro WHERE idMembro = ?",
                (id_membro,)
            )
            row = cursor.fetchone()

            if row:
                return Membro(
                    id=row[0], nome=row[1], empresa=row[2], nif=row[3],
                    email=row[4], telemovel=row[5], plano_id=row[6],
                    data_inicio=row[7], data_fim=row[8], ativo=row[9]
                )
            return None

        except pyodbc.Error as erro:
            print(f"Erro no MembroRepository, get_member_info: {erro}")
            return None
        finally:
            if conexao:
                conexao.close()

    def get_Membros(self) -> list[Membro]:
        conexao = None
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM Membro")
            rows = cursor.fetchall()

            membros = []
            for row in rows:
                membros.append(
                    Membro(
                        id=row[0], nome=row[1], empresa=row[2], nif=row[3],
                        email=row[4], telemovel=row[5], plano_id=row[6],
                        data_inicio=row[7], data_fim=row[8], ativo=row[9]
                    )
                )
            return membros

        except pyodbc.Error as erro:
            print(f"Erro no MembroRepository, get_Membros: {erro}")
            return []
        finally:
            if conexao:
                conexao.close()
