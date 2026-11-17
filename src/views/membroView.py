import tkinter as tk
from tkinter import messagebox

from src.controllers.membroController import MembroController


class MembroView:
    def __init__(self, root, utilizador_id, callback_voltar=None):
        self.root = root
        self.utilizador_id = utilizador_id
        self.callback_voltar = callback_voltar
        self.membro_controller = MembroController()
        self.membro_info = None

        self.atualizar_dados_membro()

        if self.membro_info is None:
            resposta = messagebox.askyesno(
                "Registo de Membro",
                "Ainda não tem um perfil de membro.\nDeseja registar-se agora?"
            )
            if resposta:
                self.registar_membro_form()
            else:
                if self.callback_voltar:
                    self.callback_voltar()
                self.root.destroy()
                return

        self.criar_menu_principal()

    def atualizar_dados_membro(self):
        # O utilizador_info[1] contém o ID do membro associado,
        # de acordo com a utilização já feita no MembroController.
        try:
            utilizador_info = (
                self.membro_controller.utilizador_controller
                .get_utilizador_info(self.utilizador_id)
            )

            if utilizador_info and len(utilizador_info) > 1 and utilizador_info[1]:
                self.membro_info = self.membro_controller.get_member_info(
                    utilizador_info[1]
                )
            else:
                self.membro_info = None
        except Exception as erro:
            print("Erro ao obter perfil do membro:", erro)
            self.membro_info = None

    # T2.1 e T2.2 - Registo de membro
    def registar_membro_form(self):
        top = tk.Toplevel(self.root)
        top.title("Registo de Membro")
        top.geometry("400x370")
        top.resizable(False, False)

        tk.Label(
            top, text="Registo de Membro", font=("Arial", 14, "bold")
        ).pack(pady=12)

        frame = tk.LabelFrame(top, text="Dados Profissionais")
        frame.pack(fill="both", expand=True, padx=15, pady=8)

        self.nome_var = tk.StringVar()
        self.empresa_var = tk.StringVar()
        self.nif_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.telemovel_var = tk.StringVar()

        campos = [
            ("Nome:", self.nome_var),
            ("Empresa:", self.empresa_var),
            ("NIF:", self.nif_var),
            ("Email:", self.email_var),
            ("Telefone:", self.telemovel_var)
        ]

        for texto, variavel in campos:
            linha = tk.Frame(frame)
            linha.pack(fill="x", padx=10, pady=5)
            tk.Label(linha, text=texto, width=12, anchor="w").pack(side="left")
            tk.Entry(linha, textvariable=variavel, width=30).pack(side="left")

        def registar():
            nome = self.nome_var.get().strip()
            empresa = self.empresa_var.get().strip()
            nif = self.nif_var.get().strip()
            email = self.email_var.get().strip()
            telefone = self.telemovel_var.get().strip()

            if not all([nome, empresa, nif, email, telefone]):
                messagebox.showwarning(
                    "Aviso", "Todos os campos são obrigatórios.", parent=top
                )
                return

            if len(nif) != 9 or not nif.isdigit():
                messagebox.showwarning(
                    "Aviso", "O NIF deve conter exatamente 9 dígitos.", parent=top
                )
                return

            if "@" not in email or "." not in email:
                messagebox.showwarning("Aviso", "Email inválido.", parent=top)
                return

            if len(telefone) != 9 or not telefone.isdigit():
                messagebox.showwarning(
                    "Aviso", "O telefone deve conter exatamente 9 dígitos.", parent=top
                )
                return

            sucesso = self.membro_controller.registar_membro(
                self.utilizador_id, nome, empresa, nif, email, telefone
            )

            if sucesso:
                messagebox.showinfo(
                    "Sucesso", "Membro registado com sucesso!", parent=top
                )
                top.destroy()
                self.atualizar_dados_membro()
                if self.membro_info and hasattr(self, "lbl_bem_vindo"):
                    self.lbl_bem_vindo.config(
                        text=f"Bem-vindo, {self.membro_info.nome}!"
                    )
            else:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível registar o membro. Verifique se o NIF já existe.",
                    parent=top
                )

        tk.Button(top, text="Registar", command=registar).pack(pady=12)

    # Mantém compatibilidade com chamadas da versão anterior.
    def abrir_janela_registo(self):
        self.registar_membro_form()

    # T2.3 e T2.4 - Perfil com Labels e edição com Entry
    def ver_detalhes_perfil(self):
        self.atualizar_dados_membro()

        if not self.membro_info:
            messagebox.showerror("Erro", "Dados do membro não disponíveis.")
            return

        top = tk.Toplevel(self.root)
        top.title("O Meu Perfil")
        top.geometry("450x470")
        top.resizable(False, False)

        tk.Label(top, text="O Meu Perfil", font=("Arial", 14, "bold")).pack(pady=12)

        frame = tk.LabelFrame(top, text="Dados do Membro")
        frame.pack(fill="both", expand=True, padx=15, pady=8)

        # Todos os dados do perfil são apresentados inicialmente em Labels.
        dados = [
            ("ID:", "id", False),
            ("Nome:", "nome", True),
            ("Empresa:", "empresa", True),
            ("NIF:", "nif", True),
            ("Email:", "email", True),
            ("Telefone:", "telemovel", True),
            ("Plano ID:", "plano_id", False),
            ("Data de início:", "data_inicio", False),
            ("Data de fim:", "data_fim", False),
            ("Ativo:", "ativo", False)
        ]

        self.perfil_vars = {}
        self.perfil_labels = {}
        self.perfil_entries = {}
        self.campos_editaveis = []

        for linha_num, (texto, atributo, editavel) in enumerate(dados):
            tk.Label(frame, text=texto, width=15, anchor="w").grid(
                row=linha_num, column=0, padx=8, pady=4, sticky="w"
            )

            valor = getattr(self.membro_info, atributo, "")
            if atributo == "ativo":
                valor = "Sim" if valor else "Não"

            variavel = tk.StringVar(value=str(valor if valor is not None else ""))
            self.perfil_vars[atributo] = variavel

            lbl = tk.Label(frame, textvariable=variavel, anchor="w", width=30)
            lbl.grid(row=linha_num, column=1, padx=8, pady=4, sticky="w")
            self.perfil_labels[atributo] = lbl

            if editavel:
                self.campos_editaveis.append(atributo)

        def editar():
            for atributo in self.campos_editaveis:
                self.perfil_labels[atributo].grid_remove()

                entry = tk.Entry(
                    frame, textvariable=self.perfil_vars[atributo], width=30
                )
                linha = self.campos_editaveis.index(atributo) + 1
                # Os campos editáveis ocupam as linhas 1 a 5.
                entry.grid(row=linha, column=1, padx=8, pady=4, sticky="w")
                self.perfil_entries[atributo] = entry

            btn_editar.config(state="disabled")
            btn_guardar.config(state="normal")

        def guardar():
            valores = {
                atributo: self.perfil_vars[atributo].get().strip()
                for atributo in self.campos_editaveis
            }

            if not all(valores.values()):
                messagebox.showwarning(
                    "Aviso", "Todos os campos são obrigatórios.", parent=top
                )
                return

            nif = valores["nif"]
            if len(nif) != 9 or not nif.isdigit():
                messagebox.showwarning(
                    "Aviso", "O NIF deve conter exatamente 9 dígitos.", parent=top
                )
                return

            email = valores["email"]
            if "@" not in email or "." not in email:
                messagebox.showwarning("Aviso", "Email inválido.", parent=top)
                return

            telefone = valores["telemovel"]
            if len(telefone) != 9 or not telefone.isdigit():
                messagebox.showwarning(
                    "Aviso", "O telefone deve conter exatamente 9 dígitos.", parent=top
                )
                return

            if not messagebox.askyesno(
                "Confirmar", "Deseja guardar as alterações?", parent=top
            ):
                return

            sucesso = self.membro_controller.atualizar_membro(
                self.membro_info.id,
                valores["nome"],
                valores["empresa"],
                valores["nif"],
                valores["email"],
                valores["telemovel"]
            )

            if sucesso:
                messagebox.showinfo(
                    "Sucesso", "Perfil atualizado com sucesso!", parent=top
                )
                top.destroy()
                self.atualizar_dados_membro()
            else:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível atualizar o perfil. Verifique se o NIF já existe.",
                    parent=top
                )

        botoes = tk.Frame(top)
        botoes.pack(pady=10)

        btn_editar = tk.Button(botoes, text="Editar", command=editar)
        btn_editar.pack(side="left", padx=5)

        btn_guardar = tk.Button(
            botoes, text="Guardar Alterações", command=guardar, state="disabled"
        )
        btn_guardar.pack(side="left", padx=5)

    def criar_menu_principal(self):
        self.root.title("SpaceHub - Menu Membro")
        self.root.geometry("500x350")

        nome = self.membro_info.nome if self.membro_info else "Utilizador"
        self.lbl_bem_vindo = tk.Label(
            self.root, text=f"Bem-vindo, {nome}!", font=("Arial", 16, "bold")
        )
        self.lbl_bem_vindo.pack(pady=25)

        tk.Button(
            self.root, text="O Meu Perfil", width=25,
            command=self.ver_detalhes_perfil
        ).pack(pady=7)

        tk.Button(
            self.root, text="Lista de Membros", width=25,
            command=self.abrir_lista_membros
        ).pack(pady=7)

        tk.Button(
            self.root, text="Terminar Sessão", width=25,
            command=self.terminar_sessao
        ).pack(pady=7)

    # Lista de membros já existente no projeto.
    def abrir_lista_membros(self):
        top = tk.Toplevel(self.root)
        top.title("Lista de Membros")
        top.geometry("650x350")

        frame_lista = tk.Frame(top)
        frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        lista = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set)
        lista.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=lista.yview)

        frame_detalhes = tk.LabelFrame(top, text="Detalhes do Membro")
        frame_detalhes.pack(side="right", fill="both", padx=10, pady=10)

        lbl_detalhes = tk.Label(
            frame_detalhes, text="Selecione um membro.", justify="left"
        )
        lbl_detalhes.pack(anchor="w", padx=10, pady=10)

        membros = self.membro_controller.mostrar_membros() or []
        membros_dict = {}

        for indice, membro in enumerate(membros):
            lista.insert(tk.END, f"{membro.nome} - {membro.empresa}")
            membros_dict[indice] = membro

        def selecionar(event):
            selecao = lista.curselection()
            if selecao:
                membro = membros_dict.get(selecao[0])
                if membro:
                    lbl_detalhes.config(text=(
                        f"Nome: {membro.nome}\n"
                        f"Empresa: {membro.empresa}\n"
                        f"NIF: {membro.nif}\n"
                        f"Email: {membro.email}\n"
                        f"Telemóvel: {membro.telemovel}\n"
                        f"Plano ID: {membro.plano_id}\n"
                        f"Ativo: {'Sim' if membro.ativo else 'Não'}"
                    ))

        lista.bind("<<ListboxSelect>>", selecionar)

    def terminar_sessao(self):
        if self.callback_voltar:
            self.callback_voltar()
        self.root.destroy()


# Exemplo de utilização no login:
# janela_login.withdraw()
# janela_membro = tk.Toplevel(janela_login)
# MembroView(janela_membro, utilizador_id,
#            callback_voltar=janela_login.deiconify)
