import pyodbc
from db.connection import DB_CONFIG
from src.models.membro import Membro

class MembroRepository:

    def __init__(self, db_path="db/SpaceHub.db"):
        self.db_config = DB_CONFIG

    def inserir(self, nome: str, empresa: str, nif: str, email: str, telefone: str, plano_id: int, daInicio: str, daFim: str, ativo: bool) -> bool:
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO Membro (nome_membro, empresa_membro, nif_membro, email_membro, telefone_membro, plano_id, data_inicio_plano, data_fim_plano, ativo) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (nome, empresa, nif, email, telefone, plano_id, daInicio, daFim, ativo),
            )

            conexao.commit()
            conexao.close()
            return True
        except pyodbc.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return False

    def get_nif(self, nif: str):
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT * 
                FROM Membro 
                WHERE nif_membro = ?
                """,
                (nif,),
            )
            resultado = cursor.fetchone()

            conexao.close()
            return resultado
        except pyodbc.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return None

    def conectar_idMembro(self, id_utilizador: int, id_membro: int):
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE Utilizador 
                SET membro_id = ?, perfil = 'MEMBER'
                WHERE id_utilizador = ?
                """,
                (id_membro, id_utilizador),
            )

            conexao.commit()
            conexao.close()
            return True
        except pyodbc.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return False

    def get_member_info(self, idMembro: int) -> Membro:
        try:
            conn = pyodbc.connect(self.db_config)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM Membro
                WHERE idMembro = ?
                """,
                (idMembro)
            )
            member_info = cursor.fetchone()
            conn.commit()
            conn.close()
            return member_info
        except pyodbc.Error as e:
            print(f"\n[Erro Base de Dados] {e}")
            return None
