import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.membroController import MembroController


class MembroView:
    def __init__(self, root, utilizador_id, callback_voltar=None):
        self.root = root
        self.utilizador_id = utilizador_id
        self.callback_voltar = callback_voltar
        self.membro_controller = MembroController()

        # Verifica se o utilizador já tem perfil de membro
        self.membro_info = self.membro_controller.get_member_info(self.utilizador_id)

        # Se não tiver perfil, abre formulário de registo antes do dashboard principal
        if not self.membro_info:
            if messagebox.askyesno("Aviso", "Ainda não tem um perfil de Membro associado.\nDeseja registar-se como Membro agora?"):
                self.abrir_janela_registo()
            else:
                if self.callback_voltar:
                    self.callback_voltar()
                self.root.destroy()
                return

        self.criar_menu_principal()

    def criar_menu_principal(self):
        # "Menu SpaceHub" (janela principal após login)
        self.root.title("SpaceHub - Menu Membro")
        self.root.geometry("500x450")
        self.root.config(bg="#f0f2f5")

        nome_utilizador = self.membro_info.nome if self.membro_info else "Utilizador"

        # Label de boas-vindas
        lbl_bem_vindo = tk.Label(
            self.root, 
            text=f"Bem-vindo, {nome_utilizador}!", 
            font=("Arial", 16, "bold"), 
            bg="#f0f2f5", 
            fg="#333333"
        )
        lbl_bem_vindo.pack(pady=20)

        # Frame com Botões
        frame_botoes = tk.Frame(self.root, bg="#f0f2f5")
        frame_botoes.pack(pady=10)

        btn_perfil = tk.Button(
            frame_botoes, text="O Meu Perfil", width=25, height=2, 
            bg="#007bff", fg="white", font=("Arial", 10, "bold"),
            command=self.ver_detalhes_perfil
        )
        btn_perfil.pack(pady=5)

        btn_lista = tk.Button(
            frame_botoes, text="Lista de Membros", width=25, height=2, 
            bg="#17a2b8", fg="white", font=("Arial", 10, "bold"),
            command=self.abrir_lista_membros
        )
        btn_lista.pack(pady=5)

        btn_sair = tk.Button(
            frame_botoes, text="Terminar Sessão", width=25, height=2, 
            bg="#dc3545", fg="white", font=("Arial", 10, "bold"),
            command=self.terminar_sessao
        )
        btn_sair.pack(pady=5)

        # Painel de estatísticas: LabelFrame "Espaço SpaceHub"
        self.criar_painel_estatisticas()

    def criar_painel_estatisticas(self):
        frame_stats = tk.LabelFrame(self.root, text=" Espaço SpaceHub ", font=("Arial", 10, "bold"), bg="#f0f2f5", fg="#555")
        frame_stats.pack(fill="x", padx=20, pady=15)

        self.lbl_total_membros = tk.Label(frame_stats, text="Total de Membros registados: A carregar...", bg="#f0f2f5", font=("Arial", 9))
        self.lbl_total_membros.pack(anchor="w", padx=10, pady=2)

        btn_atualizar_stats = tk.Button(frame_stats, text="Atualizar", font=("Arial", 8), command=self.atualizar_estatisticas)
        btn_atualizar_stats.pack(anchor="e", padx=10, pady=5)

        self.atualizar_estatisticas()

    def atualizar_estatisticas(self):
        membros = self.membro_controller.mostrar_membros()
        total = len(membros) if membros else 0
        self.lbl_total_membros.config(text=f"Total de Membros registados: {total}")

    def ver_detalhes_perfil(self):
        if not self.membro_info:
            messagebox.showerror("Erro", "Informações de membro não disponíveis.")
            return
        
        detalhes = (
            f"Nome: {self.membro_info.nome}\n"
            f"Empresa: {self.membro_info.empresa}\n"
            f"NIF: {self.membro_info.nif}\n"
            f"Email: {getattr(self.membro_info, 'email', 'N/D')}\n"
            f"Telemóvel: {getattr(self.membro_info, 'telemovel', 'N/D')}"
        )
        messagebox.showinfo("O Meu Perfil", detalhes)

    def abrir_lista_membros(self):
        # Janela "Lista de Membros" (Toplevel)
        top = tk.Toplevel(self.root)
        top.title("Lista de Membros")
        top.geometry("700x400")

        # Frame esquerdo para Listbox e Scrollbar
        frame_left = tk.Frame(top)
        frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_left)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame_left, yscrollcommand=scrollbar.set, font=("Courier", 10))
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Frame direito para painel lateral de detalhes
        frame_right = tk.LabelFrame(top, text=" Detalhes do Membro ", font=("Arial", 10, "bold"), width=250)
        frame_right.pack(side="right", fill="both", padx=10, pady=10)
        frame_right.pack_propagate(False)

        lbl_detalhe = tk.Label(frame_right, text="Selecione um membro\nna lista.", justify="left", font=("Arial", 9))
        lbl_detalhe.pack(anchor="w", padx=10, pady=10)

        # Obter dados através de membro_controller.mostrar_membros()
        membros = self.membro_controller.mostrar_membros()
        
        # Mapeamento para guardar os objetos associados aos índices da listbox
        membros_dict = {}
        if membros:
            for idx, m in enumerate(membros):
                # T3.4 — Formato "Nome — Empresa"
                texto_linha = f"{m.nome} — {m.empresa}"
                listbox.insert(tk.END, texto_linha)
                membros_dict[idx] = m

        # Evento de seleção na Listbox (<<ListboxSelect>>)
        def ao_selecionar(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                m = membros_dict.get(index)
                if m:
                    texto_detalhes = (
                        f"Nome: {m.nome}\n\n"
                        f"Empresa: {m.empresa}\n"
                        f"NIF: {m.nif}\n"
                        f"Email: {getattr(m, 'email', 'N/D')}\n"
                        f"Telemóvel: {getattr(m, 'telemovel', 'N/D')}\n"
                        f"Plano ID: {m.plano_id}\n"
                        f"Ativo: {'Sim' if m.ativo else 'Não'}"
                    )
                    lbl_detalhe.config(text=texto_detalhes)

        listbox.bind('<<ListboxSelect>>', ao_selecionar)

    def abrir_janela_registo(self):
        top_reg = tk.Toplevel(self.root)
        top_reg.title("Registo de Membro")
        top_reg.geometry("350x400")

        tk.Label(top_reg, text="Registo de Membro", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(top_reg, text="Nome:").pack(anchor="w", padx=20)
        entry_nome = tk.Entry(top_reg, width=35)
        entry_nome.pack(padx=20)

        tk.Label(top_reg, text="Empresa:").pack(anchor="w", padx=20)
        entry_empresa = tk.Entry(top_reg, width=35)
        entry_empresa.pack(padx=20)

        tk.Label(top_reg, text="NIF:").pack(anchor="w", padx=20)
        entry_nif = tk.Entry(top_reg, width=35)
        entry_nif.pack(padx=20)

        tk.Label(top_reg, text="Email:").pack(anchor="w", padx=20)
        entry_email = tk.Entry(top_reg, width=35)
        entry_email.pack(padx=20)

        tk.Label(top_reg, text="Telemóvel:").pack(anchor="w", padx=20)
        entry_tel = tk.Entry(top_reg, width=35)
        entry_tel.pack(padx=20)

        def submeter_registo():
            sucesso = self.membro_controller.registar_membro(
                self.utilizador_id,
                entry_nome.get(),
                entry_empresa.get(),
                entry_nif.get(),
                entry_email.get(),
                entry_tel.get()
            )
            if sucesso:
                messagebox.showinfo("Sucesso", f"Membro '{entry_nome.get()}' registado com sucesso!")
                self.membro_info = self.membro_controller.get_member_info(self.utilizador_id)
                top_reg.destroy()
                # Atualiza a janela principal se necessário
            else:
                messagebox.showerror("Erro", "Falha ao registar o membro.")

        tk.Button(top_reg, text="Registar", bg="#28a745", fg="white", width=20, command=submeter_registo).pack(pady=20)

    def terminar_sessao(self):
        # Terminar Sessão fecha a janela e reabre a de autenticação (callback)
        if self.callback_voltar:
            self.callback_voltar()
        self.root.destroy()



    # Exemplo na janela de login/autenticação:
    def abrir_menu_membro(utilizador_id):
        root.withdraw()  # Oculta a janela de login atual
        janela_membro = tk.Toplevel(root)

        # Passa a função de callback para reativar o login ao fechar/terminar sessão
        MembroView(janela_membro, utilizador_id, callback_voltar=root.deiconify)