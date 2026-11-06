from db.connection import data_base_config
from src.views.membroView import MembroView
from src.views.utilizadorView import UtilizadorView


def main():
    # Configuração da base de dados - Meter true caso queiras resetar a base de dados
    data_base_config(False)

    # Instancia as views principais do sistema
    view_uti = UtilizadorView()
    view_membro = MembroView()

    while True:
        # 1. Abre o menu principal do SpaceHub
        userLoged = view_uti.menu_principal()

        # Vai para o menu fluxo caso o membro esteja logado
        if userLoged >= 0:
            view_membro.fluxo_membro(userLoged)


if __name__ == "__main__":
    main()