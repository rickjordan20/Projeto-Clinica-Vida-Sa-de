# clinica_vida_saude/app/ui/tela_pacientes.py
# Tela CRUD de Pacientes — versão didática (apenas o essencial, bem comentado)

import tkinter as tk
from tkinter import ttk, messagebox
from app.models.paciente import Paciente
from app.repositories.paciente_repository import PacienteRepository
from app.repositories.consulta_repository import ConsultaRepository

class TelaPacientes(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)                 # cria um Frame ttk como “tela”
        self.paciente_repo = PacienteRepository()         # acesso ao CRUD de pacientes
        self.consulta_repo = ConsultaRepository()# usado para validar exclusão (consultas futuras)
        self._build()                            # monta os widgets
        self._load()                             # carrega registros na tabela

    def _build(self):
        self.pack(fill='both', expand=True)      # ocupa toda a área disponível
        ttk.Label(self, text='Pacientes', font=('Arial', 16, 'bold')).pack(pady=6)

        # --- Formulário ---
        form = ttk.Frame(self); form.pack(fill='x', padx=8, pady=4)

        ttk.Label(form, text='Nome:').grid(row=0, column=0, sticky='e')
        self.ent_nome = ttk.Entry(form, width=40)
        self.ent_nome.grid(row=0, column=1, sticky='we', padx=4, pady=2)

        ttk.Label(form, text='CPF:').grid(row=1, column=0, sticky='e')
        self.ent_cpf = ttk.Entry(form, width=20)
        self.ent_cpf.grid(row=1, column=1, sticky='we', padx=4, pady=2)

        ttk.Label(form, text='Nascimento (AAAA-MM-DD):').grid(row=2, column=0, sticky='e')
        self.ent_nasc = ttk.Entry(form, width=20)
        self.ent_nasc.grid(row=2, column=1, sticky='we', padx=4, pady=2)

        ttk.Label(form, text='Telefone:').grid(row=3, column=0, sticky='e')
        self.ent_tel = ttk.Entry(form, width=20)
        self.ent_tel.grid(row=3, column=1, sticky='we', padx=4, pady=2)

        #--- BOTÕES ----
        btns = ttk.Frame(self) ; btns.pack(pady=4)
        ttk.Button(btns,text="Novo", command=self._novo).grid(row=0, column=0,padx=4)
        ttk.Button(btns,text="Salvar", command=self._salvar).grid(row=0, column=1,padx=4)
        ttk.Button(btns,text="Excluir", command=self._exclur).grid(row=0, column=2,padx=4)
        ttk.Button(btns,text="Buscar", command=self._buscar).grid(row=0, column=3,padx=4)
        ttk.Button(btns,text="Limpar", command=self._limpar).grid(row=0, column=4,padx=4)

        # --- TABELA ----
        self.tree = ttk.Treeview(self, columns=('ID','NOME','CPF','NASC','TEL'),
                                 show='headings',height=10)
        for col, text, width in(
            ('ID','ID',40),('NOME','Nome',200),('CPF','CPF',120),
            ('NASC','Nascimento',120),('TEL','Telefone',120)
        ):
            self.tree.heading(col,text=text) #montando o cabeçalho
            self.tree.column(col,width,anchor="w") #definindo a largura das col

        self.tree.pack(fill="both",expand=True,padx=8,pady=6)
        #pega a ação de clique na lista da tabela
        self.tree.bind("<<TreeViewSelect>>",self._on_select) 
        self.sel_id = None # guarda o ID selecionado na tabela 

    def _load(self,items=None):
        #limpa e renova a tabela (com busca ou tudo)
        for i in self.tree.get_children(): #pecorrer todos os widgets filhos da tabela
            self.tree.delete(i) #deleta todos widgets dentro da tabela
        items = items or self.paciente_repo.find() 
        # acessa a função find() da classe paciente_repo e retorna uma ""lista de Paciente""
        for p in items: # pecorre a Lista de Pacientes(x,y,z..) e acessa os atributos de cada um(nome,cpf,data..)
            self.tree.insert('','end',values=(p.id,p.nome,p.cpf,p.data_nascimento or '',p.telefone or ''))
        
    def _on_select(self,_):
        #carrega registro no formulário ao clicar na tabela
        sel = self.tree.selection()    #pega qual linha da tabela a pessoa clicou
        if not sel:
            return
        self.sel_id = int(self.tree.item(sel[0],'values')[0]) #pega o ID do paciente selecionado
        p = self.paciente_repo.get_by_id(self.sel_id) #chama a função para pegar o paciente no banco com aquele ID

        if p:
            for ent, val in ((self.ent_nome,p.nome),(self.ent_cpf,p.cpf),
                             (self.ent_nasc,p.data_nascimento or ''),(self.ent_tel,p.telefone or '')):
                ent.delete(0,tk.END) #limpa o campo
                ent.insert(0,val) #insere o valor no campo

    def _novo(self): #limpa a varivel sel_id e depois a função _limpar abaixo
        self.sel_id = None 
        self._limpar()
    
    def _limpar(self): #limpa os campos de entrada do formulário
        for ent in (self.ent_nome, self.ent_cpf, self.ent_nasc, self.ent_tel):
            ent.delete(0,tk.END)


    def _salvar(self):
            # valida campos mínimos
            nome = self.ent_nome.get().strip()
            cpf  = self.ent_cpf.get().strip()
            if not nome or not cpf:
                messagebox.showwarning('Aviso', 'Nome e CPF são obrigatórios.')
                return
            p = Paciente(
                id=self.sel_id,
                nome=nome,
                cpf=cpf,
                data_nascimento=(self.ent_nasc.get().strip() or None),
                telefone=(self.ent_tel.get().strip() or None)
            )
            try:
                if p.id is None:
                    self.sel_id = self.repo.create(p)
                else:
                    self.repo.update(p)
                self._load()
            except Exception as e:
                messagebox.showerror('Erro', str(e))


    def _excluir(self):
            if self.sel_id is None:
                return
            # regra simples: alerta caso haja consultas futuras
            if self.consulta_repo.has_future_for_paciente(self.sel_id):
                messagebox.showwarning('Aviso', 'Paciente possui consultas futuras. Exclusão não recomendada.')
                return
            if messagebox.askyesno('Confirmar', 'Deseja excluir este paciente?'):
                try:
                    self.repo.delete(self.sel_id)
                    self.sel_id = None
                    self._limpar(); self._load()
                except Exception as e:
                    messagebox.showerror('Erro', str(e))


    def _buscar(self):
            nome = self.ent_nome.get().strip() or None
            cpf  = self.ent_cpf.get().strip() or None
            items = self.repo.find(nome=nome, cpf=cpf)
            if not items:
                messagebox.showinfo('Info', 'Nenhum paciente encontrado.')
            self._load(items)

        
