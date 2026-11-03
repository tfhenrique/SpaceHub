# bibliotecas
import os
from db.connection import initialize_database
from src.views.utilizadorView import UtilizadorView
from src.views.membroView import MembroView

# Iniciação dos componentes do sistema
view_uti = UtilizadorView()
view_membro = MembroView()

def main():
    # Inicializa a base de dados
    initialize_database()

    while True:
        # Exibe o menu principal e processa as opções do utilizador
        userLoged = view_uti.menu_principal()
    
        # Quand o utilizador estiver logado, chama o menu de registo de membro
        menuOperation = view_membro.registar_membro_menu(userLoged)
        if menuOperation == -2:
            continue  # Volta ao menu principal se o utilizador deslogar

if __name__ == "__main__":
    main()


