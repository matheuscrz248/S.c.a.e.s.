import tkinter as tk
from tkinter import StringVar, X, W, Y, BOTH, VERTICAL, HORIZONTAL
import tkinter.messagebox as msb
import tkinter.ttk as ttk
import sqlite3
import os
from controller.auth_controller import User


class MainView(tk.Tk):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.title("Sistema de controle de aluguéis de equipamentos de som")
        self.geometry("850x500")
        self.config(bg='#22222c')
        self.minsize(700, 400)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.cliente = StringVar()
        self.telefone = StringVar()
        self.equipamento = StringVar()
        self.marcamodelo = StringVar()
        self.valoraluguel = StringVar()
        self.id = None

        base_dir = os.path.dirname(os.path.dirname(__file__))
        db_dir = os.path.join(base_dir, "db")
        os.makedirs(db_dir, exist_ok=True)
        self.caminho_dbSCAES = os.path.join(db_dir, "SCAES.sqlite")

        self.criar_interface()
        self.databaseSCAES()

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def criar_interface(self):
        welcome_label = tk.Label(
            self,
            text=f"Bem-vindo à tela principal, {self.user.nome}!",
            font=("Helvetica", 16, "bold"),
            bg="#22222c",
            fg="#FFFFFF"
        )
        welcome_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

        tabela_frame = tk.Frame(self, bg="#22222c")
        tabela_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 10))
        tabela_frame.grid_rowconfigure(0, weight=1)
        tabela_frame.grid_columnconfigure(0, weight=1)

        ScrollbarY = tk.Scrollbar(tabela_frame, orient=VERTICAL)
        ScrollbarX = tk.Scrollbar(tabela_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            tabela_frame,
            columns=("ID", "Cliente", "Telefone", "Equipamento", "MarcaModelo", "ValorAluguel"),
            yscrollcommand=ScrollbarY.set,
            xscrollcommand=ScrollbarX.set,
            show='headings'
        )

        ScrollbarY.config(command=self.tree.yview)
        ScrollbarX.config(command=self.tree.xview)
        ScrollbarY.grid(row=0, column=1, sticky='ns')
        ScrollbarX.grid(row=1, column=0, sticky='ew')
        self.tree.grid(row=0, column=0, sticky='nsew')

        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Equipamento", text="Equipamento")
        self.tree.heading("MarcaModelo", text="Marca e modelo")
        self.tree.heading("ValorAluguel", text="Valor do aluguel")

        self.tree.column("ID", width=30, stretch=False)
        self.tree.column("Cliente", width=180, stretch=False)
        self.tree.column("Telefone", width=120, stretch=False)
        self.tree.column("Equipamento", width=120, stretch=False)
        self.tree.column("MarcaModelo", width=220, stretch=False)
        self.tree.column("ValorAluguel", width=120, stretch=False)

        self.tree.bind("<Double-1>", self.selecionar_dado)

        botoes = tk.Frame(self, bg="#22222c")
        botoes.grid(row=2, column=0, pady=5)

        estilo_botao = {"width": 12, "height": 1, "font": ("Arial", 12, "bold")}

        tk.Button(botoes, text="Gerar relatório", bg="darkgreen", fg="white",
                  command=self.gerar_relatorio, **estilo_botao).pack(side='left', padx=10)

        tk.Button(botoes, text="Adicionar", bg="royal blue", fg="white", command=self.inserir_dados, **estilo_botao).pack(side='left', padx=10)
        tk.Button(botoes, text="Apagar", bg="OrangeRed2", fg="white", command=self.apagar_dado, **estilo_botao).pack(side='left', padx=10)

        sair_btn = tk.Button(
            self,
            text="Sair",
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            width=8,
            height=1,
            command=self.confirmar_saida
        )
        sair_btn.place(x=20, y=self.winfo_height() - 10)
        self.bind("<Configure>", lambda e: sair_btn.place(x=20, y=self.winfo_height() - 40))

        mensagem = tk.Label(self, text="Para alterar clique duas vezes na seleção.",
                            bg="#22222c", fg="white", font=("Arial", 10))
        mensagem.grid(row=3, column=0, pady=(5, 10))

    def gerar_relatorio(self):
        import re

        resposta = msb.askyesno("Confirmação", "Deseja realmente gerar o relatório dos dados?")
        if not resposta:
            return

        conn = sqlite3.connect(self.caminho_dbSCAES)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM humanos WHERE usuario_id = ? ORDER BY cliente", (self.user.id,))
        dados = cursor.fetchall()
        conn.close()

        if not dados:
            msb.showinfo("Relatório", "Nenhum dado encontrado para gerar relatório.")
            return

        relatorio_texto = f"RELATÓRIO DE ALUGUÉIS\nUsuário: {self.user.nome}\n\n"
        for row in dados:
            relatorio_texto += (
                f"ID: {row[0]}\n"
                f"Cliente: {row[1]}\n"
                f"Telefone: {row[2]}\n"
                f"Equipamento: {row[3]}\n"
                f"Marca/Modelo: {row[4]}\n"
                f"Valor: {row[5]}\n"
                f"{'-'*40}\n"
            )

        janela_relatorio = tk.Toplevel(self)
        janela_relatorio.title("Relatório")
        janela_relatorio.geometry("500x400")

        text_area = tk.Text(janela_relatorio, wrap='word')
        text_area.insert("1.0", relatorio_texto)
        text_area.config(state='disabled')
        text_area.pack(expand=True, fill=BOTH, padx=10, pady=10)

        nome_usuario_limpo = re.sub(r'[^\w]', '', self.user.nome)  
        pasta = os.path.dirname(self.caminho_dbSCAES)
        indice = 1

        while True:
            nome_arquivo = f"relatorio({nome_usuario_limpo})({indice}).txt"
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            if not os.path.exists(caminho_arquivo):
                break
            indice += 1

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(relatorio_texto)

        msb.showinfo("Relatório", f"Relatório salvo com sucesso em:\n{caminho_arquivo}")


    def confirmar_saida(self):
        resposta = msb.askyesno("Confirmação", "Tem certeza que deseja sair para tela de login?")
        if resposta:
            self.voltar_para_login()

    def voltar_para_login(self):
        from view.login_view import LoginView
        self.destroy()
        login = LoginView()
        login.mainloop()

    def databaseSCAES(self):
        conn = sqlite3.connect(self.caminho_dbSCAES)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS humanos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                telefone TEXT,
                equipamento TEXT,
                marcamodelo TEXT,
                valoraluguel TEXT,
                usuario_id INTEGER
            )
        """)
        conn.commit()
        cursor.execute("SELECT * FROM humanos WHERE usuario_id = ? ORDER BY cliente", (self.user.id,))
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()

    def enviar_dados(self):
        if not all([self.cliente.get(), self.telefone.get(), self.equipamento.get(), self.marcamodelo.get(), self.valoraluguel.get()]):
            msb.showwarning("", "Por favor, preencha todos os campos.", icon="warning")
            return
        conn = sqlite3.connect(self.caminho_dbSCAES)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO humanos (cliente, telefone, equipamento, marcamodelo, valoraluguel, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.cliente.get(), self.telefone.get(), self.equipamento.get(),
            self.marcamodelo.get(), self.valoraluguel.get(), self.user.id
        ))
        conn.commit()
        cursor.execute("SELECT * FROM humanos WHERE usuario_id = ? ORDER BY cliente", (self.user.id,))
        self.tree.delete(*self.tree.get_children())
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()
        for var in [self.cliente, self.telefone, self.equipamento, self.marcamodelo, self.valoraluguel]:
            var.set("")

    def apagar_dado(self):
        if not self.tree.selection():
            msb.showwarning('Erro', 'Selecione um item para deletar.')
            return
        if msb.askyesno('Confirmação', 'Deseja realmente deletar a seleção?'):
            item = self.tree.selection()[0]
            valores = self.tree.item(item, 'values')
            conn = sqlite3.connect(self.caminho_dbSCAES)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM humanos WHERE id = ? AND usuario_id = ?", (valores[0], self.user.id))
            conn.commit()
            conn.close()
            self.tree.delete(item)

    def selecionar_dado(self, event):
        item = self.tree.selection()
        if not item:
            return
        dados = self.tree.item(item[0])['values']
        self.id = dados[0]
        self.cliente.set(dados[1])
        self.telefone.set(dados[2])
        self.equipamento.set(dados[3])
        self.marcamodelo.set(dados[4])
        self.valoraluguel.set(dados[5])

        self.janela_alterar = tk.Toplevel(self)
        self.janela_alterar.title("Atualizar aluguel")
        self.janela_alterar.geometry("400x300")
        form = tk.Frame(self.janela_alterar)
        form.pack(expand=True, fill=BOTH, padx=20, pady=20)

        campos = ['Cliente', 'Telefone', 'Equipamento', 'Marca e modelo', 'Valor do aluguel']
        variaveis = [self.cliente, self.telefone, self.equipamento, self.marcamodelo, self.valoraluguel]
        for i, (campo, var) in enumerate(zip(campos, variaveis)):
            tk.Label(form, text=campo, anchor='w').grid(row=i, column=0, sticky=W)
            tk.Entry(form, textvariable=var).grid(row=i, column=1, sticky="ew", padx=5, pady=5)
        form.columnconfigure(1, weight=1)

        tk.Button(form, text="Atualizar", command=self.alterar_dados).grid(row=len(campos), columnspan=2, pady=10)

    def alterar_dados(self):
        conn = sqlite3.connect(self.caminho_dbSCAES)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE humanos SET cliente=?, telefone=?, equipamento=?, marcamodelo=?, valoraluguel=?
            WHERE id=? AND usuario_id=?
        """, (
            self.cliente.get(), self.telefone.get(), self.equipamento.get(),
            self.marcamodelo.get(), self.valoraluguel.get(), self.id, self.user.id
        ))
        conn.commit()
        cursor.execute("SELECT * FROM humanos WHERE usuario_id = ? ORDER BY cliente", (self.user.id,))
        self.tree.delete(*self.tree.get_children())
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()
        self.janela_alterar.destroy()

    def inserir_dados(self):
        for var in [self.cliente, self.telefone, self.equipamento, self.marcamodelo, self.valoraluguel]:
            var.set("")

        self.janela_incluir = tk.Toplevel(self)
        self.janela_incluir.title("Inserir aluguel")
        self.janela_incluir.geometry("400x300")
        form = tk.Frame(self.janela_incluir)
        form.pack(expand=True, fill=BOTH, padx=20, pady=20)

        campos = ['Cliente', 'Telefone', 'Equipamento', 'Marca e modelo', 'Valor do aluguel']
        variaveis = [self.cliente, self.telefone, self.equipamento, self.marcamodelo, self.valoraluguel]
        for i, (campo, var) in enumerate(zip(campos, variaveis)):
            tk.Label(form, text=campo, anchor='w').grid(row=i, column=0, sticky=W)
            tk.Entry(form, textvariable=var).grid(row=i, column=1, sticky="ew", padx=5, pady=5)
        form.columnconfigure(1, weight=1)

        tk.Button(form, text="Cadastrar", command=self.enviar_dados).grid(row=len(campos), columnspan=2, pady=10)
