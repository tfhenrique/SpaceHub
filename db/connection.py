from pathlib import Path
import pyodbc
import time, os, subprocess

# Parâmetros de configuração para a ligação ao SQL Server
SERVER_NAME = "DESKTOP-NI0HD87"
DATABASE_NAME = "SpaceHub"

# Ligação à base de dados 'master' (usada para criar a SpaceHub se não existir)
MASTER_CONFIG = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER_NAME};"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)

# Ligação normal à base de dados SpaceHub
DB_CONFIG = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    "Trusted_Connection=yes;"
)

# método responsável por efetuar todas as funções no main
def data_base_config(resetDataBase: bool):
    # Limpa a consola
    subprocess.run(["cls" if os.name == "nt" else "clear"], shell=True)
    print("\033[96mA Iniciar base de dados...\033[0m")
    time.sleep(1)
    # Reinicia a database, meter False caso não queiras reiniciar a database
    reinitialize_database(resetDataBase)
    time.sleep(1)
    # Inicializa a base de dados do SQL Server
    initialize_database()
    time.sleep(1)
    # Testa a conecxão
    testar_conexao()
    time.sleep(1)
    print("\033[96mA iniciar programa...\033[0m")
    time.sleep(3)

# Testa a conecxão com a base de dados
def testar_conexao():
    try:
        # Abre a conexão utilizando a string configurada
        conn = pyodbc.connect(DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT @@SERVERNAME, @@VERSION")
        row = cursor.fetchone()

        print("\033[92mLigação ao SQL Server bem-sucedida!\033[0m")
        print(f"\033[96mServidor: {row[0]}\033[0m")
        print(f"\033[96mVersão: {row[1][:50]}...\033[0m")

        conn.close()
        return True

    except pyodbc.Error as e:
        print(f"\033[91mErro ao ligar à base de dados: {e}\033[0m")
        return False

# Cria as tabelas dentro da base de dados
def initialize_database():
    schema_path = Path("db/schema.sql")

    if not schema_path.exists():
        print(f"\033[93mAviso: O ficheiro {schema_path} não foi encontrado.\033[0m")
        return

    try:
        # autocommit=True é útil para executar comandos de criação de tabelas/esquemas
        conn = pyodbc.connect(MASTER_CONFIG, autocommit=True)
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT name 
            FROM sys.databases 
            WHERE name = '{DATABASE_NAME}'
            """
        )
        resultado = cursor.fetchone()

        if not resultado:
            # Lê o conteúdo do schema.sql com pathlib
            schema_sql = schema_path.read_text(encoding="utf-8")
    
            # Como o pyodbc não o interpreta nativamente, dividimos o texto por 'GO' (em maiúsculas ou minúsculas) para executar comando a comando.
            batches = schema_sql.split("GO")
    
            for batch in batches:
                if batch.strip():
                    cursor.execute(batch)

        print("\033[92mEsquema da base de dados inicializado com sucesso no SQL Server!\033[0m")
        conn.close()
    except pyodbc.Error as e:
        print(f"\033[91mErro ao inicializar o esquema no SQL Server: {e}\033[0m")

# Reinicia a base de dados para alterações
def reinitialize_database(reset: bool):
    try:
        if(reset):
            config_master = DB_CONFIG.replace("DATABASE=SpaceHub;", "DATABASE=master;")
            
            conn = pyodbc.connect(config_master, autocommit=True)
            cursor = conn.cursor()

            print("\033[93mAviso: A eliminar Base de Dados\033[0m")
            # Verifica se a base de dados existe nas tabelas de sistema
            cursor.execute(
                """
                IF EXISTS (SELECT * FROM sys.databases WHERE name = 'SpaceHub')
                BEGIN
                    DROP DATABASE SpaceHub;
                END
                """
            )
            conn.close()
    except pyodbc.Error as e:
        print(f"\n\033[91m[Erro ao eliminar a Base de Dados] {e}\033[0m")