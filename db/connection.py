import pyodbc

# Parâmetros de configuração para a ligação ao SQL Server
SERVER_NAME = 'DESKTOP-NI0HD87\\SQLEXPRESS'
DATABASE_NAME = 'SpaceHub'

# String de conexão usando Autenticação do Windows (Trusted_Connection)
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
        
        print("Ligação bem-sucedida!")
        print(f"Servidor: {row[0]}")
        print(f"Versão: {row[1][:50]}")
        
    except pyodbc.Error as e:
        print(f"Erro ao ligar à base de dados: {e}")
        
    finally:
        # Garante que a conexão é fechada mesmo se ocorrer um erro
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    testar_conexao()