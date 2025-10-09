# Tela CRUD de Médicos - usa oi campo "horario_atendimento"  (ex:08:00-17:00)

import tkinter as tk
from tkinter import ttk, messagebox 
from app.models.medico import Medico

from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medico_repository import MedicoRepository

class TelaMedicos(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.medico_repo = MedicoRepository()
        self.consulta_repo = ConsultaRepository()
        self._build()
        self._load()

    def _build(self):
        self.pack(fill='both',expand=True) #expande a frame(responsividade)
        ttk.Label(self ,text="Médicos",font=("Arial",16,"bold")).pack(pady=6)

        #Criando um container para o formulário
        form = ttk.Frame(self) ; form.pack(fill="x",padx=8,pady=4)

        #Criando Label e Input de Nome na tela do formulário
        ttk.Label(form,text="Nome").grid(row=0,column=0,sticky="e")
        self.ent_nome = ttk.Entry(form,width=40)
        self.ent_nome.grid(row=0,column=1,sticky="we",padx=4,pady=2)

        #Criando Label e Input de CRM na tela do formulário
        ttk.Label(form,text="CRM").grid(row=1,column=0,sticky="e")
        self.ent_CRM = ttk.Entry(form,width=20)
        self.ent_CRM.grid(row=1,column=1,sticky="we",padx=4,pady=2)

        #Criando Label e Input de ESPECIALIDADE na tela do formulário
        ttk.Label(form,text="Especialidade").grid(row=2,column=0,sticky="e")
        self.ent_esp = ttk.Entry(form,width=20)
        self.ent_esp.grid(row=2,column=1,sticky="we",padx=4,pady=2)

        #Criando Label e Input de HORÁRIO DE ATENDIMENTO na tela do formulário
        ttk.Label(form,text="Horário de Atendimento (ex:08:00-17:00)").grid(row=3,column=0,sticky="e")
        self.ent_hor = ttk.Entry(form,width=20)
        self.ent_hor.grid(row=3,column=1,sticky="we",padx=4,pady=2)
        self.ent_hor.insert(0,"08:00-17:00")

        btns = ttk.Frame(self) ; btns.pack(pady=4)

        ttk.Button(btns, text="Novo", command=self._novo).grid(row=0,column=0,padx=4)
        ttk.Button(btns,text="Salvar",command=self._salvar).grid(row=0, column=1, padx=4)
        #ttk.Button(btns,text="Excluir",command=self._excluir).grid(row=0,column=2,padx=4)
        ttk.Button(btns,text="Buscar",command=self._buscar).grid(row=0, column=3, padx=4)
        ttk.Button(btns,text="Limpar",command=self._limpar).grid(row=0, column=4, padx=4)
        
        #CRIAÇÃO DE TABELA COM COLUNAS
        self.tree = ttk.Treeview(self,columns=("id","nome","crm","esp","hor"),
                                 show="headings",height=10)
        #show=headings -> mostrar os títulos do cabeçalho
        for col, text, width in (
            ('id','ID',40),('nome','Nome',180), ('crm','CRM',100),
            ('esp','Especialidade',140), ('hor','Atendimento',120)
        ):
            self.tree.heading(col,text=text) #cria o cabebeçalho com as colunas
            self.tree.column(col,width=width,anchor="w") #configura as colunas
        
        self.tree.pack(fill='both',expand=True) #deixa a tabela responsiva
        self.tree.bind('<<TreeViewSelect>>',
                       self._on_select) #captura algum evento do usuário com a tela 

    def _on_select(self, items = None):
        sel = self.tree.selection() #retorna uma tupla de seleção da tabela médicos
        if not sel: #se não tiver nada na var "sel", retorna nada
            return
        self.sel_id = int(self.tree.item(sel[0],'values')[0]) 
            #pegar o indice do registro do Medico        
        m = self.medico_repo.get_by_id(self.sel_id) 
            #pega exatamente o OBJETO médico atraves do ID
        if m:
            for ent, val in (
                (self.ent_nome,m.nome),(self.ent_CRM,m.crm),
                (self.ent_esp,m.especialidade or '')
                (self.ent_hor,m.horario_atendimento or ''
                 )
            ):
                ent.delete(0,tk.END)
                ent.insert(0,val)
    
    def _load(self, items=None):
        for i in self.tree.get_children(): #Pega o WIDGET da TABELA TREE(FILHO)
            self.tree.delete(i) #Deleta todos WIDGETS da TABELA TREE
            
        items = items or self.medico_repo.find() 
            #recebe um valor do parametro "items" ou 
            # chama a função find da classe medico_repo

        for m in items: #Preenche a tabela novamente com a info do medico
            self.tree.insert('','end',values=(m.id,m.nome,
            m.crm,m.especialidade or '',m.horario_atendimento or ''))

    def _novo(self):
        self.sel_id = None
        self._limpar()

    def _limpar(self):
        for ent in (self.ent_nome,self.ent_CRM,
                    self.ent_esp,self.ent_hor):
            ent.delete(0,tk.END)
    
    def _salvar(self):
        nome = self.ent_nome.get().strip() 
            #GET ->pega o valor ; STRIP->Apaga os espacos em branco

        crm = self.ent_CRM.get().strip()
            #GET ->pega o valor ; STRIP->Apaga os espacos em branco
        
        if not nome or not crm:
            messagebox.showwarning("AVISO",
                                   "Nome e CRM são obrigatórios!")
            return
        
        especiliade = self.ent_esp.get().strip() or None
        horario_atendimento = self.ent_hor.get().strip() or None

        m = Medico(id=self.sel_id,nome=nome,crm=crm,
                   especialidade=especiliade,horario_atendimento=horario_atendimento)
        try:
            if m.id is None: #se o ID do atributo do médico estiver vazio
                self.sel_id = self.medico_repo.create(m) 
                    #pega o id da seleção e coloca para criar o novo médico
            else:
                self.medico_repo.update(m) 
                    #atualiza os dados com o médico existente quando selecionado
        except Exception as e:
            messagebox.showerror("ERRO",str(e))

    def _buscar(self):
        items = self.medico_repo.find(
            nome= self.ent_nome.get().strip(),
            crm= self.ent_CRM.get().strip(),
            especialidade= self.ent_esp.get().strip() or None
        )
        if not items:
            messagebox.showinfo("INFO","Nenhum médico encontrado!")
                
            
        
        
        





