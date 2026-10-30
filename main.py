# bibliotecas
import os
from db.connection import initialize_database
from src.views.utilizadorView import UtilizadorView

# Iniciação dos componentes do sistema
view_uti = UtilizadorView()

def main():
    # Inicializa a base de dados
    initialize_database()

    # Exibe o menu principal e processa as opções do utilizador
    view_uti.menu_principal()

if __name__ == "__main__":
    main()


