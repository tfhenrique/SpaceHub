from db.connection import initialize_database, reinitialize_database
from src.views.membroView import MembroView
from src.views.utilizadorView import UtilizadorView


def main():
    # Reinicia a database, meter False caso não queiras reiniciar a database
    reinitialize_database(True)
    # Inicializa a base de dados do SQL Server
    initialize_database()

    # Instancia as views principais do sistema
    view_uti = UtilizadorView()
    view_membro = MembroView()

    while True:
        # 1. Abre o menu principal do SpaceHub
        userLoged = view_uti.menu_principal()

        # Vai para o menu fluxo caso o membro esteja logado
        if userLoged:
            view_membro.fluxo_membro(userLoged)


if __name__ == "__main__":
    main()