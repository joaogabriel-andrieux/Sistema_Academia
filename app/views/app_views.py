import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests

BASE_URL = "http://127.0.0.1:5000"

class SplashScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Carregando...")
        self.geometry("450x250")
        self.configure(bg="#2c3e50") 
        self.overrideredirect(True)
        self._centralizar_janela()

        tk.Label(self, text="GYM MANAGEMENT", font=("Arial", 18, "bold"), fg="white", bg="#2c3e50").pack(pady=(40, 5))
        tk.Label(self, text="Sistema de Gestão de Academia", font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50").pack()
        
        self.progresso = ttk.Progressbar(self, mode="indeterminate", length=300)
        self.progresso.pack(pady=30)
        self.progresso.start(15)

        self.after(3000, self.verificar_api_e_continuar)

    def _centralizar_janela(self):
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def verificar_api_e_continuar(self):
        try:
            requests.get(f"{BASE_URL}/alunos", timeout=2)
            api_online = True
        except:
            api_online = False

        self.progresso.stop()
        self.destroy()
        
        if api_online:
            app_login = TelaLogin()
            app_login.mainloop()
        else:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar à API Flask. Ative o back-end primeiro!")



import json
import os

INSTRUTORES_FILE = "instrutores.json"

def carregar_instrutores():
    if not os.path.exists(INSTRUTORES_FILE):
        admin_padrao = [{"nome": "Administrador", "cpf": "000.000.000-00", "telefone": "(00) 00000-0000", "login": "admin", "senha": "admin"}]
        with open(INSTRUTORES_FILE, "w", encoding="utf-8") as f:
            json.dump(admin_padrao, f, ensure_ascii=False, indent=2)
        return admin_padrao
        
    try:
        with open(INSTRUTORES_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if not isinstance(dados, list):
                return [{"nome": "Administrador", "cpf": "000.000.000-00", "telefone": "(00) 00000-0000", "login": "admin", "senha": "admin"}]
            return dados
    except Exception:
        return [{"nome": "Administrador", "cpf": "000.000.000-00", "telefone": "(00) 00000-0000", "login": "admin", "senha": "admin"}]

def salvar_instrutor(novo):
    instrutores = carregar_instrutores()
    instrutores.append(novo)
    with open(INSTRUTORES_FILE, "w", encoding="utf-8") as f:
        json.dump(instrutores, f, ensure_ascii=False, indent=2)


class TelaLogin:
    def __init__(self, master=None):
        if master is None:
            self.window = tk.Tk()
        else:
            self.window = tk.Toplevel(master)
            
        self.window.title("Login - Sistema de Academia")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.configure(bg="white")
        
        self._centralizar_janela()
        
        if master is None:
            self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
        else:
            self.window.protocol("WM_DELETE_WINDOW", master.destroy)
            
        self._build_ui()

    def mainloop(self, *args, **kwargs):
        self.window.mainloop(*args, **kwargs)

    def _centralizar_janela(self):
        self.window.update_idletasks()
        largura = self.window.winfo_width()
        altura = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.window.winfo_screenheight() // 2) - (altura // 2)
        self.window.geometry(f"{largura}x{altura}+{x}+{y}")

    def _build_ui(self):
        tk.Label(self.window, text="🔑 Sistema de Academia", font=("Arial", 16, "bold"), bg="white").pack(pady=30)

        tk.Label(self.window, text="Login", font=("Arial", 10), bg="white").pack()
        self.entry_login = tk.Entry(self.window, width=30)
        self.entry_login.pack(pady=5)
        self.entry_login.insert(0, "admin")

        tk.Label(self.window, text="Senha", font=("Arial", 10), bg="white").pack()
        self.entry_senha = tk.Entry(self.window, show="*", width=30)
        self.entry_senha.pack(pady=5)
        self.entry_senha.insert(0, "admin")

        tk.Button(self.window, text="Entrar", width=20, command=self.fazer_login, bg="#2ecc71", fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        tk.Button(self.window, text="Cadastrar Instrutor", width=20, command=self.abrir_cadastro, font=("Arial", 10)).pack()

    def fazer_login(self):
        import requests
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        try:
            # Consulta a API em vez de ler o arquivo local
            response = requests.get("http://127.0.0.1:5000/personais")
            
            if response.status_code == 200:
                personais = response.json()
                
                # Procura se existe alguém com aquele usuario e senha na lista que veio da API
                usuario_valido = next((p for p in personais if p['usuario'] == login and p.get('senha') == senha), None)
                
                if usuario_valido:
                    self.window.destroy()
                    # Se for o 'admin', abre a lista, senão abre o painel
                    if login == "admin":
                        # TelaListaInstrutores(personais) # Certifique-se de que essa tela exista
                        messagebox.showinfo("Sucesso", "Bem-vindo Admin!")
                    else:
                        self._abrir_painel_principal()
                else:
                    messagebox.showerror("Erro", "Login ou senha inválidos.", parent=self.window)
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao servidor.", parent=self.window)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro de conexão: {e}", parent=self.window)
    def _abrir_painel_principal(self):
        try:
            PainelHub()
        except TypeError:
            PainelHub(None)

    def abrir_cadastro(self):
        TelaCadastroInstrutor(self.window)


class TelaCadastroInstrutor(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Instrutor")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(bg="white")
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="📋 Cadastro de Instrutor", font=("Arial", 14, "bold"), bg="white").pack(pady=20)

        campos = [
            ("Nome completo", "entry_nome",     ""),
            ("CPF",           "entry_cpf",      ""),
            ("Telefone",      "entry_telefone", ""),
            ("Login",         "entry_login",    ""),
            ("Senha",         "entry_senha",    "*"),
            ("Confirmar senha","entry_confirma","*"),
        ]
        for label, attr, show in campos:
            tk.Label(self, text=label, font=("Arial", 10), bg="white").pack(anchor="w", padx=50, pady=(3,0))
            entry = tk.Entry(self, show=show, width=30)
            entry.pack(pady=2)
            setattr(self, attr, entry)

        tk.Button(self, text="Salvar Cadastro", width=20, command=self.colher_dados, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

    def colher_dados(self):
        import requests  # Garante que a biblioteca está importada para fazer o envio HTTP

        nome     = self.entry_nome.get().strip()
        cpf      = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        login    = self.entry_login.get().strip()
        senha    = self.entry_senha.get().strip()
        confirma = self.entry_confirma.get().strip()

        # 1. Validações locais simples (para poupar requisição desnecessária)
        if not all([nome, cpf, login, senha, confirma]):
            messagebox.showwarning("Atenção", "Todos os campos (incluindo CPF) são obrigatórios para o backend.", parent=self)
            return

        # Valida CPF: precisa ter exatamente 11 dígitos numéricos
        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showwarning("CPF inválido", "O CPF deve conter exatamente 11 números, sem pontos ou traços.", parent=self)
            return

        # Valida telefone (se foi preenchido): precisa ter 10 ou 11 dígitos numéricos
        if telefone and (not telefone.isdigit() or len(telefone) not in (10, 11)):
            messagebox.showwarning("Telefone inválido", "O telefone deve conter 10 ou 11 números, sem parênteses ou traços.", parent=self)
            return

        # Valida senha: mínimo de 6 caracteres
        if len(senha) < 6:
            messagebox.showwarning("Senha inválida", "A senha deve ter no mínimo 6 caracteres.", parent=self)
            return

        if senha != confirma:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=self)
            return

        # 2. Monta o dicionário com as chaves exatas que o reqparse da API está esperando
        payload = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone if telefone else "",
            "usuario": login,  # O backend espera 'usuario'
            "senha": senha
        }

        try:
            # 3. Dispara o POST para a rota que acabamos de validar no navegador!
            url = "http://127.0.0.1:5000/personais"
            response = requests.post(url, json=payload)

            # Se o backend aceitou e salvou (Status 201 Created)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", f"Personal '{nome}' cadastrado com sucesso no banco!", parent=self)
                self.destroy()
            
            # Se o backend recusou (ex: CPF ou usuário duplicado - Status 400)
            elif response.status_code == 400:
                erro_api = response.json().get("message", "Erro na validação dos dados.")
                messagebox.showerror("Erro no Cadastro", erro_api, parent=self)
            
            else:
                messagebox.showerror("Erro", f"Erro inesperado no servidor: {response.status_code}", parent=self)

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor. O Flask está rodando?", parent=self)
class TelaListaInstrutores(tk.Tk):
    def __init__(self, lista_instrutores):
        super().__init__()
        self.title("Painel do Administrador - Gerenciar Personais")
        self.geometry("600x450")
        self.configure(bg="#f8f9fa")
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (450 // 2)
        self.geometry(f"600x450+{x}+{y}")
        
        tk.Label(self, text="👥 Personais Cadastrados no Sistema", font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(pady=15)
        
        frame_lista = tk.Frame(self, bg="white", bd=1, relief="solid")
        frame_lista.pack(padx=20, pady=10, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_lista, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        header_font = ("Arial", 10, "bold")
        tk.Label(scrollable_frame, text="Nome", font=header_font, bg="white", width=20, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(scrollable_frame, text="CPF", font=header_font, bg="white", width=15, anchor="w").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(scrollable_frame, text="Telefone", font=header_font, bg="white", width=15, anchor="w").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(scrollable_frame, text="Usuário", font=header_font, bg="white", width=12, anchor="w").grid(row=0, column=3, padx=5, pady=5)
        
        tk.Frame(scrollable_frame, height=2, bg="#bdc3c7", width=550).grid(row=1, column=0, columnspan=4, sticky="we", pady=5)
        
        idx = 2
        for inst in lista_instrutores:
            if not isinstance(inst, dict):
                continue
            bg_row = "#f9f9f9" if idx % 2 == 0 else "white"
            
            nome_instrutor = inst.get("nome", "Sem Nome")
            cpf_instrutor  = inst.get("cpf", "Não informado")
            tel_instrutor  = inst.get("telefone", "Não informado")
            login_instrutor = inst.get("login", "Sem Usuário")
            
            tk.Label(scrollable_frame, text=nome_instrutor, bg=bg_row, width=20, anchor="w").grid(row=idx, column=0, padx=5, pady=3)
            tk.Label(scrollable_frame, text=cpf_instrutor, bg=bg_row, width=15, anchor="w").grid(row=idx, column=1, padx=5, pady=3)
            tk.Label(scrollable_frame, text=tel_instrutor, bg=bg_row, width=15, anchor="w").grid(row=idx, column=2, padx=5, pady=3)
            tk.Label(scrollable_frame, text=login_instrutor, bg=bg_row, width=12, anchor="w").grid(row=idx, column=3, padx=5, pady=3)
            idx += 1

        tk.Button(self, text="Ir para o Painel da Academia ➔", command=self.avancar, bg="#34495e", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5).pack(pady=20)

    def avancar(self):
        self.destroy()
        try:
            PainelHub()
        except TypeError:
            PainelHub(None)
class PainelHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GymManagement - Painel Principal")
        self.geometry("620x250")
        self.configure(bg="#f8f9fa")
        self.resizable(False, False)
        self._centralizar_janela()

        tk.Label(self, text="🏋️ SELECIONE O MÓDULO DE GESTÃO", font=("Arial", 13, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(pady=25)

        frame_blocos = tk.Frame(self, bg="#f8f9fa")
        frame_blocos.pack(pady=10)

        estilo_bloco = {
            "font": ("Arial", 10, "bold"),
            "bg": "#e2e8f0",
            "fg": "#2d3748",
            "activebackground": "#cbd5e1",
            "padx": 10,
            "pady": 20,
            "borderwidth": 1,
            "relief": "groove",
            "width": 15,
            "cursor": "hand2"
        }

        btn_alunos = tk.Button(frame_blocos, text="👥\n\nALUNOS", command=lambda: self.abrir_modulo(0), **estilo_bloco)
        btn_alunos.pack(side="left", padx=8)

        btn_equipamentos = tk.Button(frame_blocos, text="⚙️\n\nEQUIPAMENTOS", command=lambda: self.abrir_modulo(1), **estilo_bloco)
        btn_equipamentos.pack(side="left", padx=8)

        btn_exercicios = tk.Button(frame_blocos, text="🏋️\n\nEXERCÍCIOS", command=lambda: self.abrir_modulo(2), **estilo_bloco)
        btn_exercicios.pack(side="left", padx=8)

        btn_series = tk.Button(frame_blocos, text="📋\n\nSÉRIES (TREINOS)", command=lambda: self.abrir_modulo(3), **estilo_bloco)
        btn_series.pack(side="left", padx=8)

    def _centralizar_janela(self):
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def abrir_modulo(self, indice_aba):
        self.destroy() 
        app_principal = App() 
        app_principal.notebook.select(indice_aba) 
        app_principal.mainloop()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Academia - Telas de Testes")
        self.geometry("1000x750")
        self.configure(bg="white")
        
        btn_voltar = tk.Button(self, text="⬅ Voltar ao Menu Principal", font=("Arial", 9, "bold"), bg="#4a5568", fg="white", borderwidth=0, padx=10, pady=5, command=self.voltar_ao_hub)
        btn_voltar.pack(anchor="w", padx=15, pady=(10, 0))

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Treeview", 
                        background="#ffffff", 
                        foreground="#333333", 
                        rowheight=28, 
                        fieldbackground="#ffffff", 
                        borderwidth=0)
        
        estilo.configure("Treeview.Heading", 
                        background="#1a365d", 
                        foreground="white", 
                        font=("Arial", 10, "bold"), 
                        padding=6)
        estilo.map("Treeview.Heading", background=[('active', '#2a4365')])

        estilo.configure("TNotebook", background="#edf2f7", borderwidth=0)
        estilo.configure("TNotebook.Tab", 
                        background="#cbd5e0", 
                        foreground="#4a5568", 
                        padding=[15, 6], 
                        font=("Arial", 9, "bold"))
        estilo.map("TNotebook.Tab", 
                  background=[("selected", "#1a365d")], 
                  foreground=[("selected", "#ffffff")])

        estilo.configure("TButton", 
                        background="#e2e8f0", 
                        foreground="#2d3748", 
                        font=("Arial", 9, "bold"), 
                        padding=[10, 6], 
                        borderwidth=0, 
                        relief="flat")
        estilo.map("TButton", background=[("active", "#cbd5e0")])

        estilo.configure("Success.TButton", background="#48bb78", foreground="white")
        estilo.map("Success.TButton", background=[("active", "#38a169"), ("disabled", "#e2e8f0")], foreground=[("disabled", "#a0aec0")])

        estilo.configure("Danger.TButton", background="#e53e3e", foreground="white")
        estilo.map("Danger.TButton", background=[("active", "#c53030")])
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabelas = {}

        self.criar_aba_alunos()
        self.criar_aba_equipamentos()
        self.criar_aba_exercicios()
        self.criar_aba_series()

    def voltar_ao_hub(self):
        self.destroy()
        hub = PainelHub()
        hub.mainloop()

    def carregar_dados(self, tree, endpoint):
        for row in tree.get_children():
            tree.delete(row)
        try:
            response = requests.get(f"{BASE_URL}/{endpoint}")
            if response.status_code == 200:
                for item in response.json():
                    tree.insert("", "end", values=list(item.values()))
        except:
            pass

    def criar_aba_alunos(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" 👤 Alunos ")

        frame_inputs = ttk.LabelFrame(aba, text=" Cadastro de Alunos ")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_inputs, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_id = ttk.Label(frame_inputs, text="")
        lbl_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        txt_nome = ttk.Entry(frame_inputs, width=40)
        txt_nome.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Matrícula:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        txt_matr = ttk.Entry(frame_inputs, width=20)
        txt_matr.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        colunas = ("id", "nome", "matricula")
        tree = ttk.Treeview(aba, columns=colunas, show="headings")
        tree.heading("id", text="Id")
        tree.heading("nome", text="Nome")
        tree.heading("matricula", text="Matrícula")

        tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabelas["alunos"] = tree

        def selecionar(event):
            item = tree.selection()
            if item:
                val = tree.item(item, "values")
                lbl_id.config(text=val[0])
                txt_nome.delete(0, tk.END)
                txt_nome.insert(0, val[1])
                txt_matr.delete(0, tk.END)
                txt_matr.insert(0, val[2])

        tree.bind("<<TreeviewSelect>>", selecionar)

        def incluir():
            nome = txt_nome.get().strip()
            matricula = txt_matr.get().strip()
            if not nome or not matricula: 
                messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha o Nome e a Matrícula do aluno antes de incluir!")
                return
            res = requests.post(f"{BASE_URL}/alunos", json={"nome": nome, "matricula": matricula})
            if res.status_code == 201:
                limpar()
                self.carregar_dados(tree, "alunos")
                

        def alterar():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione um aluno na tabela antes de clicar em Alterar!")
                return
            btn_salvar.config(state="normal") 

        def salvar():
            idx = lbl_id.cget("text")
            if not idx: return
            
            nome = txt_nome.get().strip()
            matricula = txt_matr.get().strip()
            
            if not nome or not matricula:
                messagebox.showwarning("Campos Obrigatórios", "O Nome e a Matrícula não podem ficar vazios!")
                return
                
            res = requests.put(f"{BASE_URL}/alunos/{idx}", json={"nome": nome, "matricula": matricula})
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
                limpar()
                self.carregar_dados(tree, "alunos")

        def excluir():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione um aluno na tabela antes de clicar em Excluir!")
                return
            
            resposta = messagebox.askyesno(
                "Confirmar Exclusão", 
                "Deseja realmente excluir este aluno?"
            )
            
            if resposta:
                res = requests.delete(f"{BASE_URL}/alunos/{idx}")
                if res.status_code == 200:
                    messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                    limpar()
                    self.carregar_dados(tree, "alunos")

        def limpar():
            lbl_id.config(text="")
            txt_nome.delete(0, tk.END)
            txt_matr.delete(0, tk.END)
            tree.selection_remove(tree.selection())
            btn_salvar.config(state="disabled") 

        f_botoes = ttk.Frame(aba)
        f_botoes.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(f_botoes, text="Incluir", command=incluir, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Alterar", command=alterar).pack(side="left", padx=5)
        
        btn_salvar = ttk.Button(f_botoes, text="Salvar", state="disabled", command=salvar, style="Success.TButton")
        btn_salvar.pack(side="left", padx=5)
        
        ttk.Button(f_botoes, text="Excluir", command=excluir, style="Danger.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

        self.carregar_dados(tree, "alunos")

    def criar_aba_equipamentos(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" ⚙️ Equipamentos ")

        frame_inputs = ttk.LabelFrame(aba, text=" Cadastro de Equipamentos ")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_inputs, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_id = ttk.Label(frame_inputs, text="")
        lbl_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        txt_nome = ttk.Entry(frame_inputs, width=40)
        txt_nome.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Marca:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        txt_marca = ttk.Entry(frame_inputs, width=20)
        txt_marca.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Carga Máxima (kg):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        txt_peso = ttk.Entry(frame_inputs, width=15)
        txt_peso.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        colunas = ("id", "nome", "marca", "peso_maximo", "status")
        tree = ttk.Treeview(aba, columns=colunas, show="headings")
        
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("marca", text="Marca")
        tree.heading("peso_maximo", text="Carga Máxima (kg)")
        tree.heading("status", text="Status")

        tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabelas["equipamentos"] = tree

        def selecionar(event):
            item = tree.selection()
            if item:
                val = tree.item(item, "values")
                lbl_id.config(text=val[0])
                txt_nome.delete(0, tk.END)
                txt_nome.insert(0, val[1])
                txt_marca.delete(0, tk.END)
                txt_marca.insert(0, val[2])
                txt_peso.delete(0, tk.END)
                txt_peso.insert(0, val[3])

        tree.bind("<<TreeviewSelect>>", selecionar)

        def incluir():
            nome = txt_nome.get().strip()
            marca = txt_marca.get().strip()
            peso_texto = txt_peso.get().strip()

            if not nome or not marca: 
                messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha o Nome e a Marca do equipamento!")
                return

            try:
                peso_valor = float(peso_texto if peso_texto else 0)
                if peso_valor <= 0:
                    messagebox.showwarning("Aviso de Validação", "Erro: A Carga Máxima não pode ser um valor negativo ou zero!")
                    return
            except ValueError:
                messagebox.showwarning("Aviso de Validação", "Erro: Digite um número válido para a Carga Máxima!")
                return

            res = requests.post(f"{BASE_URL}/equipamentos", json={"nome": nome, "marca": marca, "peso_maximo": peso_valor})
            if res.status_code == 201:
                limpar()
                self.carregar_dados(tree, "equipamentos")

        def alterar():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione um equipamento na tabela antes de clicar em Alterar!")
                return
            btn_salvar.config(state="normal") 

        def salvar():
            idx = lbl_id.cget("text")
            if not idx: return

            nome = txt_nome.get().strip()
            marca = txt_marca.get().strip()
            peso_texto = txt_peso.get().strip()

            if not nome or not marca:
                messagebox.showwarning("Campos Obrigatórios", "O Nome e a Marca não podem ficar vazios!")
                return

            try:
                peso_valor = float(peso_texto if peso_texto else 0)
                if peso_valor <= 0:
                    messagebox.showwarning("Aviso de Validação", "Erro: A Carga Máxima não pode ser um valor negativo ou zero!")
                    return
            except ValueError:
                messagebox.showwarning("Aviso de Validação", "Erro: Digite um número válido para a Carga Máxima!")
                return

            res = requests.put(f"{BASE_URL}/equipamentos/{idx}", json={"nome": nome, "marca": marca, "peso_maximo": peso_valor})
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
                limpar()
                self.carregar_dados(tree, "equipamentos")

        def excluir():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione um equipamento na tabela antes de clicar em Excluir!")
                return
            
            resposta = messagebox.askyesno(
                "Confirmar Exclusão", 
                "Deseja realmente excluir este equipamento?"
            )
            
            if resposta:
                res = requests.delete(f"{BASE_URL}/equipamentos/{idx}")
                if res.status_code == 200:
                    messagebox.showinfo("Sucesso", "Equipamento excluído com sucesso!")
                    limpar()
                    self.carregar_dados(tree, "equipamentos")

        def limpar():
            lbl_id.config(text="")
            txt_nome.delete(0, tk.END)
            txt_marca.delete(0, tk.END)
            txt_peso.delete(0, tk.END)
            tree.selection_remove(tree.selection())
            btn_salvar.config(state="disabled") 

        f_botoes = ttk.Frame(aba)
        f_botoes.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(f_botoes, text="Incluir", command=incluir, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Alterar", command=alterar).pack(side="left", padx=5)
        
        btn_salvar = ttk.Button(f_botoes, text="Salvar", state="disabled", command=salvar, style="Success.TButton")
        btn_salvar.pack(side="left", padx=5)
        
        ttk.Button(f_botoes, text="Excluir", command=excluir, style="Danger.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

        self.carregar_dados(tree, "equipamentos")

    def criar_aba_exercicios(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" 🏋️ Exercícios ")

        frame_inputs = ttk.LabelFrame(aba, text=" Cadastro de Exercícios ")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_inputs, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_id = ttk.Label(frame_inputs, text="")
        lbl_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        txt_nome = ttk.Entry(frame_inputs, width=40)
        txt_nome.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Grupo Muscular:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        txt_grupo = ttk.Entry(frame_inputs, width=20)
        txt_grupo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="ID Equipamento:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        txt_eq_id = ttk.Entry(frame_inputs, width=10)
        txt_eq_id.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        colunas = ("id", "nome", "grupo_muscular", "equipamento_id")
        tree = ttk.Treeview(aba, columns=colunas, show="headings")
        
        tree.heading("id", text="Id")
        tree.heading("nome", text="Nome")
        tree.heading("grupo_muscular", text="Grupo muscular")
        tree.heading("equipamento_id", text="Equipamento id")

        tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabelas["exercicios"] = tree

        def selecionar(event):
            item = tree.selection()
            if item:
                val = tree.item(item, "values")
                lbl_id.config(text=val[0])
                txt_nome.delete(0, tk.END)
                txt_nome.insert(0, val[1])
                txt_grupo.delete(0, tk.END)
                txt_grupo.insert(0, val[2])
                txt_eq_id.delete(0, tk.END)
                txt_eq_id.insert(0, val[3])

        tree.bind("<<TreeviewSelect>>", selecionar)

        def incluir():
            nome = txt_nome.get().strip()
            grupo = txt_grupo.get().strip()
            eq_id = txt_eq_id.get().strip()
            
            if not nome or not grupo or not eq_id:
                messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos antes de incluir!")
                return

            try:
                eq_id_num = int(eq_id)
                if eq_id_num <= 0:
                    messagebox.showwarning("Aviso de Validação", "Erro: O ID do Equipamento deve ser um número maior que zero!")
                    return
            except ValueError:
                messagebox.showwarning("Aviso de Validação", "Erro: Digite um número válido para o ID do Equipamento!")
                return

            res = requests.post(f"{BASE_URL}/exercicios", json={
                "nome": nome, 
                "grupo_muscular": grupo, 
                "equipamento_id": eq_id_num
            })
            
            if res.status_code == 201:
                limpar()
                self.carregar_dados(tree, "exercicios")
            else:
                messagebox.showerror("Erro de Cadastro", "Não foi possível cadastrar o exercício. Verifique se o ID do Equipamento realmente existe!")

        def alterar():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione um exercício na tabela antes de clicar em Alterar!")
                return
            btn_salvar.config(state="normal") 

        def salvar():
            idx = lbl_id.cget("text")
            if not idx: return

            nome = txt_nome.get().strip()
            grupo = txt_grupo.get().strip()
            eq_id = txt_eq_id.get().strip()

            if not nome or not grupo or not eq_id:
                messagebox.showwarning("Campos Obrigatórios", "Nenhum campo pode ficar vazio!")
                return

            try:
                eq_id_num = int(eq_id)
                if eq_id_num <= 0:
                    messagebox.showwarning("Aviso de Validação", "Erro: O ID do Equipamento deve ser um número maior que zero!")
                    return
            except ValueError:
                messagebox.showwarning("Aviso de Validação", "Erro: Digite um número válido para o ID do Equipamento!")
                return

            res = requests.put(f"{BASE_URL}/exercicios/{idx}", json={
                "nome": nome, 
                "grupo_muscular": grupo, 
                "equipamento_id": eq_id_num
            })
            
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
                limpar()
                self.carregar_dados(tree, "exercicios")
            else:
                messagebox.showerror("Erro ao Salvar", "Não foi possível salvar as alterações. Verifique se o ID do Equipamento realmente existe!")

        def excluir():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione um exercício na tabela antes de clicar em Excluir!")
                return
            
            resposta = messagebox.askyesno(
                "Confirmar Exclusão", 
                "Deseja realmente excluir este exercício?"
            )
            
            if resposta:
                res = requests.delete(f"{BASE_URL}/exercicios/{idx}")
                if res.status_code == 200:
                    messagebox.showinfo("Sucesso", "Exercício excluído com sucesso!")
                    limpar()
                    self.carregar_dados(tree, "exercicios")

        def limpar():
            lbl_id.config(text="")
            txt_nome.delete(0, tk.END)
            txt_grupo.delete(0, tk.END)
            txt_eq_id.delete(0, tk.END)
            tree.selection_remove(tree.selection())
            btn_salvar.config(state="disabled") 

        f_botoes = ttk.Frame(aba)
        f_botoes.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(f_botoes, text="Incluir", command=incluir, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Alterar", command=alterar).pack(side="left", padx=5)
        
        btn_salvar = ttk.Button(f_botoes, text="Salvar", state="disabled", command=salvar, style="Success.TButton")
        btn_salvar.pack(side="left", padx=5)
        
        ttk.Button(f_botoes, text="Excluir", command=excluir, style="Danger.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

        self.carregar_dados(tree, "exercicios")

    def criar_aba_series(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" 📋 Séries ")

        frame_inputs = ttk.LabelFrame(aba, text=" Ficha de Treino / Séries ")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        # FUNÇÕES DE VALIDAÇÃO EM TEMPO REAL
        def validar_apenas_numeros(texto_novo):
            return texto_novo == "" or texto_novo.isdigit()

        def validar_peso(texto_novo):
            if texto_novo == "":
                return True
            return texto_novo.replace('.', '', 1).isdigit()

        vcmd_int = (aba.register(validar_apenas_numeros), "%P")
        vcmd_float = (aba.register(validar_peso), "%P")

        ttk.Label(frame_inputs, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_id = ttk.Label(frame_inputs, text="")
        lbl_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="ID Aluno:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        txt_aluno = ttk.Entry(frame_inputs, width=10, validate="key", validatecommand=vcmd_int)
        txt_aluno.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        txt_aluno.focus()  # O cursor já inicia piscando aqui!

        ttk.Label(frame_inputs, text="ID Exercício:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        txt_ex = ttk.Entry(frame_inputs, width=10, validate="key", validatecommand=vcmd_int)
        txt_ex.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Qtd Séries:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        txt_qtd = ttk.Entry(frame_inputs, width=10, validate="key", validatecommand=vcmd_int)
        txt_qtd.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Repetições:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        txt_rep = ttk.Entry(frame_inputs, width=10, validate="key", validatecommand=vcmd_int)
        txt_rep.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_inputs, text="Carga Peso (kg):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        txt_peso = ttk.Entry(frame_inputs, width=10, validate="key", validatecommand=vcmd_float)
        txt_peso.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Frame único para os botões (será empacotado no rodapé)
        f_botoes = ttk.Frame(aba)

        colunas = ("id", "aluno_id", "exercicio_id", "quantidade_series", "repeticoes", "carga_peso")
        tree = ttk.Treeview(aba, columns=colunas, show="headings")
        
        tree.heading("id", text="Id")
        tree.heading("aluno_id", text="Aluno id")
        tree.heading("exercicio_id", text="Exercício id")
        tree.heading("quantidade_series", text="Quantidade de séries")
        tree.heading("repeticoes", text="Repetições")
        tree.heading("carga_peso", text="Carga peso (kg)")
        self.tabelas["series"] = tree

        def selecionar(event):
            item = tree.selection()
            if item:
                val = tree.item(item, "values")
                lbl_id.config(text=val[0])
                txt_aluno.delete(0, tk.END)
                txt_aluno.insert(0, val[1])
                txt_ex.delete(0, tk.END)
                txt_ex.insert(0, val[2])
                txt_qtd.delete(0, tk.END)
                txt_qtd.insert(0, val[3])
                txt_rep.delete(0, tk.END)
                txt_rep.insert(0, val[4])
                txt_peso.delete(0, tk.END)
                txt_peso.insert(0, val[5])

        tree.bind("<<TreeviewSelect>>", selecionar)

        def incluir():
            aluno_id = txt_aluno.get().strip()
            exercicio_id = txt_ex.get().strip()
            peso_texto = txt_peso.get().strip()

            if not aluno_id or not exercicio_id: 
                messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha o ID Aluno e o ID Exercício!")
                return

            try:
                peso_valor = float(peso_texto if peso_texto else 0)
                if peso_valor <= 0:
                    messagebox.showwarning("Aviso de Validação", "Erro: A carga peso não pode ser um valor negativo ou zero!")
                    return
            except ValueError:
                messagebox.showwarning("Aviso de Validação", "Erro: Digite um número válido para a carga peso!")
                return

            res = requests.post(f"{BASE_URL}/series", json={
                "aluno_id": int(aluno_id), 
                "exercicio_id": int(exercicio_id),
                "quantidade_series": int(txt_qtd.get() or 3), 
                "repeticoes": int(txt_rep.get() or 10),
                "carga_peso": peso_valor
            })
            if res.status_code == 201:
                limpar()
                self.carregar_dados(tree, "series")
            else:
                messagebox.showerror("Erro de Cadastro", "Não foi possível cadastrar a série. Verifique se o ID do Aluno e o ID do Exercício realmente existem!")

        def alterar():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione uma série na tabela antes de clicar em Alterar!")
                return
            btn_salvar.config(state="normal") 

        def salvar():
            idx = lbl_id.cget("text")
            if not idx: return

            aluno_id = txt_aluno.get().strip()
            exercicio_id = txt_ex.get().strip()
            peso_texto = txt_peso.get().strip()

            if not aluno_id or not exercicio_id:
                messagebox.showwarning("Campos Obrigatórios", "Os campos ID Aluno e ID Exercício não podem ficar vazios!")
                return

            try:
                peso_valor = float(peso_texto if peso_texto else 0)
                if peso_valor <= 0:
                    messagebox.showwarning("Aviso de Validação", "Erro: A carga peso não pode ser um valor negativo ou zero!")
                    return
            except ValueError:
                messagebox.showwarning("Aviso de Validação", "Erro: Digite um número válido para a carga peso!")
                return

            res = requests.put(f"{BASE_URL}/series/{idx}", json={
                "aluno_id": int(aluno_id), 
                "exercicio_id": int(exercicio_id),
                "quantidade_series": int(txt_qtd.get() or 3), 
                "repeticoes": int(txt_rep.get() or 10),
                "carga_peso": peso_valor
            })
            
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
                limpar()
                self.carregar_dados(tree, "series")
            else:
                messagebox.showerror("Erro ao Salvar", "Não foi possível salvar as alterações. Verifique se os IDs informados realmente existem!")

        def excluir():
            idx = lbl_id.cget("text")
            if not idx: 
                messagebox.showwarning("Aviso", "Selecione uma série na tabela antes de clicar em Excluir!")
                return
            
            resposta = messagebox.askyesno(
                "Confirmar Exclusão", 
                "Deseja realmente excluir esta série?"
            )
            
            if resposta:
                res = requests.delete(f"{BASE_URL}/series/{idx}")
                if res.status_code == 200:
                    messagebox.showinfo("Sucesso", "Série excluída com sucesso!")
                    limpar()
                    self.carregar_dados(tree, "series")

        def limpar():
            lbl_id.config(text="")
            txt_aluno.delete(0, tk.END)
            txt_ex.delete(0, tk.END)
            txt_qtd.delete(0, tk.END)
            txt_rep.delete(0, tk.END)
            txt_peso.delete(0, tk.END)
            tree.selection_remove(tree.selection())
            btn_salvar.config(state="disabled") 
            txt_aluno.focus()  # O cursor retorna para o ID Aluno automaticamente

        # Configuração estruturada dos botões
        ttk.Button(f_botoes, text="Incluir", command=incluir, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Alterar", command=alterar).pack(side="left", padx=5)
        
        btn_salvar = ttk.Button(f_botoes, text="Salvar", state="disabled", command=salvar, style="Success.TButton")
        btn_salvar.pack(side="left", padx=5)
        
        ttk.Button(f_botoes, text="Excluir", command=excluir, style="Danger.TButton").pack(side="left", padx=5)
        ttk.Button(f_botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

        # Empacotamento com Layout Trava-Rodapé
        f_botoes.pack(side="bottom", fill="x", padx=10, pady=10)
        tree.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        self.carregar_dados(tree, "series")

if __name__ == "__main__":
    app_splash = SplashScreen()
    app_splash.mainloop()