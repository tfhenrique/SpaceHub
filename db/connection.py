from pathlib import Path
import pyodbc

# Parâmetros de configuração para a ligação ao SQL Server
SERVER_NAME = "DESKTOP-NI0HD87"
DATABASE_NAME = "SpaceHub" 

# String de conexão com Autenticação do Windows (Trusted_Connection)
DB_CONFIG = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    "Trusted_Connection=yes;"
)


def testar_conexao():
    try:
        # Abre a conexão utilizando a string configurada
        conn = pyodbc.connect(DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT @@SERVERNAME, @@VERSION")
        row = cursor.fetchone()

        print("Ligação ao SQL Server bem-sucedida!")
        print(f"Servidor: {row[0]}")
        print(f"Versão: {row[1][:50]}...")

        conn.close()
        return True

    except pyodbc.Error as e:
        print(f"Erro ao ligar à base de dados: {e}")
        return False


def initialize_database():
    schema_path = Path("db/schema.sql")

    if not schema_path.exists():
        print(f"Aviso: O ficheiro {schema_path} não foi encontrado.")
        return

    try:
        # autocommit=True é útil para executar comandos de criação de tabelas/esquemas
        conn = pyodbc.connect(DB_CONFIG, autocommit=True)
        cursor = conn.cursor()

        # Lê o conteúdo do schema.sql com pathlib
        schema_sql = schema_path.read_text(encoding="utf-8")

        # Como o pyodbc não o interpreta nativamente, dividimos o texto por 'GO' (em maiúsculas ou minúsculas) para executar comando a comando.
        batches = schema_sql.split("GO")

        for batch in batches:
            if batch.strip():
                cursor.execute(batch)

        print("Esquema da base de dados inicializado com sucesso no SQL Server!")
        conn.close()

    except pyodbc.Error as e:
        print(f"Erro ao inicializar o esquema no SQL Server: {e}")


if __name__ == "__main__":
    if testar_conexao():
        initialize_database()