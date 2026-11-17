import tkinter as tk
from tkinter import messagebox
from src.controllers.utilizadorController import UtilizadorController


class UtilizadorView:

    def __init__(self):
        self.controller = UtilizadorController()
        self.utilizador_id = None  # ID do utilizador autenticado (None = sem sessão)

        
        self.root = tk.Tk()     # Janela principal
        self.root.title("SpaceHub — Gestão de Espaço")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.utilizador_var = tk.StringVar()
        self.password_var = tk.StringVar()

    def exibir_menu(self):
                                # LabelFrame de acesso
        frame = tk.LabelFrame(self.root, text="Acesso ao Sistema", padx=20, pady=20)
        frame.pack(padx=40, pady=60, fill="both")

        tk.Label(frame, text="Utilizador:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(frame, textvariable=self.utilizador_var, width=25).grid(
            row=0, column=1, pady=5, padx=5)

        tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5)
        tk.Entry(frame, textvariable=self.password_var, show="*", width=25).grid(
            row=1, column=1, pady=5, padx=5)

        tk.Button(frame, text="Entrar", width=12, command=self.entrar).grid(
            row=2, column=0, columnspan=2, pady=(15, 5))

        # Botão de registo
        tk.Button(frame, text="Criar Conta", width=12, command=self.abrir_registo).grid(
            row=3, column=0, columnspan=2, pady=5)

    def menu_principal(self): # menu_principal(): arranca o mainloop
        self.exibir_menu()
        self.root.mainloop()

    
    def entrar(self):       # Autenticar Utilizador"
        login = self.utilizador_var.get().strip()
        passhash = self.password_var.get().strip()

        if not login or not passhash:   # Campos vazios
            messagebox.showerror("Erro", "Preencha o utilizador e a password.")
            return

        if self.controller.autenticar_utilizador(login, passhash):
            self.utilizador_id = self.controller.get_utilizador_id(login)
            self.password_var.set("")
            self.abrir_janela_membro(login)
        else:   # Falha de autenticação
            messagebox.showerror("Erro", f"Falha ao autenticar o utilizador '{login}'.")     

    
    def abrir_registo(self):    #  Criar Utilizador"
        janela = tk.Toplevel(self.root)
        janela.title("Criar Conta")
        janela.geometry("350x220")
        janela.resizable(False, False)
        janela.transient(self.root)
        janela.grab_set()

        novo_user = tk.StringVar()
        nova_password = tk.StringVar()

        tk.Label(janela, text="Novo utilizador:").grid(row=0, column=0, padx=10, pady=15, sticky="e")
        tk.Entry(janela, textvariable=novo_user).grid(row=0, column=1, padx=10)

        tk.Label(janela, text="Password:").grid(row=1, column=0, padx=10, pady=15, sticky="e")
        tk.Entry(janela, textvariable=nova_password, show="*").grid(row=1, column=1, padx=10)

        def confirmar():
            login = novo_user.get().strip()
            passhash = nova_password.get().strip()

            if not login or not passhash:
                messagebox.showerror("Erro", "Preencha todos os campos.", parent=janela)
                return

            if self.controller.registar_utilizador(login, passhash):
                messagebox.showinfo(
                    "Sucesso", f"Utilizador '{login}' registado com sucesso!", parent=janela)
                janela.destroy()
            else:
                messagebox.showerror(
                    "Erro", f"Falha ao registar o utilizador '{login}'.", parent=janela)

        tk.Button(janela, text="Confirmar", width=12, command=confirmar).grid(
            row=2, column=0, columnspan=2, pady=15)

    def abrir_janela_membro(self, login):   # Transição para a janela de membro (ID fica em self.utilizador_id)
        self.root.withdraw()

        membro = tk.Toplevel(self.root)
        membro.title("SpaceHub — Área de Membro")
        membro.geometry("500x400")

        tk.Label(membro, text=f"Bem-vindo, {login}!", font=("Arial", 14)).pack(pady=40)

        def terminar_sessao():
            self.utilizador_id = None
            membro.destroy()
            self.root.deiconify()

        tk.Button(membro, text="Terminar Sessão", command=terminar_sessao).pack()
        membro.protocol("WM_DELETE_WINDOW", terminar_sessao)


if __name__ == "__main__":
    UtilizadorView().menu_principal()