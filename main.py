import tkinter as tk
from db.connection import data_base_config
from src.views.membroView import MembroView
from src.views.utilizadorView import UtilizadorView


def abrir_menu_membro(root, utilizador_id):
    # Função global para abrir o menu de membro
    janela_membro = tk.Toplevel(root)
    MembroView(janela_membro, utilizador_id, callback_voltar=root.deiconify)


def main():
    # Configuração da base de dados (True se quiser resetar a BD)
    data_base_config(False)

    # Cria a janela principal (root) do Tkinter para a aplicação
    root = tk.Tk()

    # Inicializa a vista de utilizador (janela de autenticação)
    # Usamos uma função lambda para passar o root em conjunto com o utilizador_id
    app = UtilizadorView(root, callback_sucesso_login=lambda uid: abrir_menu_membro(root, uid))

    # Inicia o loop principal da interface gráfica
    root.mainloop()


if __name__ == "__main__":
    main()