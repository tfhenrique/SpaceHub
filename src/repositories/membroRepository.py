import pyodbc
from db.connection import DB_CONFIG
from src.models.membro import Membro

class MembroRepository:

    def __init__(self, db_path="db/SpaceHub.db"):
        self.db_config = DB_CONFIG

    def inserir(self, membro: Membro) -> bool:
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO Membro (nome, empresa, NIF, email, telemovel, plano_id, data_inicio, data_fim, ativo) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (membro.nome, membro.empresa, membro.nif, membro.email, membro.telemovel, membro.plano_id, membro.data_inicio, membro.data_fim, membro.ativo),
            )

            conexao.commit()
            conexao.close()
            return True
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no MembroRepository no inserir: {e}\033[0m")
            return False

    def get_nif(self, nif: str) -> Membro | None:
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT * 
                FROM Membro 
                WHERE NIF = ?
                """,
                (nif,),
            )
            row = cursor.fetchone()
            conexao.close()
            if row:
                return Membro(
                    id=row[0],
                    nome=row[1],
                    empresa=row[2],
                    nif=row[3],
                    email=row[4],
                    telemovel=row[5],
                    plano_id=row[6],
                    data_inicio=row[7],
                    data_fim=row[8],
                    ativo=row[9]
                )
            return None
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no MembroRepository no get_nif: {e}\033[0m")
            return None

    def conectar_idMembro(self, id_utilizador: int, id_membro: int):
        try:
            conexao = pyodbc.connect(self.db_config)
            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE Utilizador 
                SET membro_id = ?, perfil = 'MEMBER'
                WHERE idUtilizador = ?
                """,
                (id_membro, id_utilizador),
            )

            conexao.commit()
            conexao.close()
            return True
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no MembroRepository no conectar_idMembro: {e}\033[0m")
            return False

    def get_member_info(self, idMembro: int) -> Membro | None:
        try:
            conn = pyodbc.connect(self.db_config)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM Membro
                WHERE idMembro = ?
                """,
                (idMembro,)
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                return Membro(
                    id=row[0],
                    nome=row[1],
                    empresa=row[2],
                    nif=row[3],
                    email=row[4],
                    telemovel=row[5],
                    plano_id=row[6],
                    data_inicio=row[7],
                    data_fim=row[8],
                    ativo=row[9]
                )
            return None
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no MembroRepository no get_member_info: {e}\033[0m")
            return None

    def get_Membros(self) -> list[Membro]:
        try:
            conn = pyodbc.connect(self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Membro")
            rows = cursor.fetchall()
            conn.close()
            
            membros = []
            for row in rows:
                membros.append(
                    Membro(
                        id=row[0],
                        nome=row[1],
                        empresa=row[2],
                        nif=row[3],
                        email=row[4],
                        telemovel=row[5],
                        plano_id=row[6],
                        data_inicio=row[7],
                        data_fim=row[8],
                        ativo=row[9]
                    )
                )
            return membros
        except pyodbc.Error as e:
            print(f"\n\033[91mErro no MembroRepository no get_all_members: {e}\033[0m")
            return []