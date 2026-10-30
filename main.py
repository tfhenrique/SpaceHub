# bibliotecas
import os
from db.connection import initialize_database
from src.views.viewUtilizador import viewUtilizador

# Iniciação dos componentes do sistema
view_uti = viewUtilizador()

def main():
    # Inicializa a base de dados
    initialize_database()

    # Exibe o menu principal e processa as opções do utilizador
    view_uti.menu_principal()

def limpar_tela():
  os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()


