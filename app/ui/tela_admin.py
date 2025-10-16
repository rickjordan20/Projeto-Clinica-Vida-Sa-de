#Tela Administrativa - Abas: (1) Usuários(crud) (2)Backup/Restore 

import tkinter as tk
from tkinter import ttk,messagebox,filedialog 
#Widgets ttk e diálogos padrão(caixa de mensagem,abrir aquivo)

import sqlite3 #Para captura erros de integridade 

from app.repositories.usuario_repository import UsuarioRepository

#from models.usuario import Usuario

# Constantes com as opções de perfil disponíveis
# para o combobox
PERFIS = ['Admin','Medico','Recepcionista']

""" A tela administrativa é um Frame ttk
que poderá ser embutido numa janela principal
"""
class TelaAdmin(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
    # Inicializa o Frame base 
    #   com o container pai(master)
        self.repo_user = UsuarioRepository()
        #Instância o repositório para operações de usuários(CRUD)
        #self.bkp = importar depois de criar bacup_service
        self.sel_user_id = None
        #Guarda o ID do usuário seleciuonado na tabela (None=nenhum)
        self._build() # Monta toda a iterface(abas, forms, botões,etc.)
        #self._user_load() # Carrega os usuários do banco e preenche o TreeView

    def _build(self):
        self.pack(fill='both', expand=True) 
            #Expande op Frame para ocupar toda area disponivel na tela

        #Título da Tela
        ttk.Label(text='Tela Admin',font=("Arial",16,"bold")).pack(pady=8)

        # Notebook (controle de abas)
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill='both',expand=True,padx=8,pady=8)
            #Expande o notebook na tela e aplica margens

        #Criar duas abas (Frames filhos do Notebook)
        self.tab_user = ttk.Frame(self.nb) # ABA DE USUÁRIOS
        self.tab_backup = ttk.Frame(self.nb) #ABA DE BACKUP E RESTORE

        self.nb.add(self.tab_user,text="Usuário") 
            #Adiciona a aba "Usuario"
        self.nb.add(self.tab_backup,text="Backup e Restore") 
            #Adiciona a aba "Backup e Restore"
        
        #Monta o conteúdo interno de caba aba
        self._build_user_tab()
        #self._build_backup_tab()

    def _build_user_tab(self):
        #Grupo de formulário de cadastro-edição
        form = ttk.LabelFrame(self.tab_user,
                              text="Cadastro de usuários")
        form.pack(fill='both',expand=True)

        #Campo Nome
        ttk.Label(form,text="Nome: ").grid(
            row=0,column=0,pady=4,padx=4,sticky='e')
         #Rotulo fica alinhado a direita 'e'
        self.ent_nome = ttk.Entry(form,width=35)
        self.ent_nome.grid(row=0,column=1,pady=4, padx=4, sticky='we')

        #Campo Login
        ttk.Label(form,text="Login: ").grid(row=1,column=0,padx=4,pady=4,sticky='e')
        self.ent_login = ttk.Entry(form,width=35)
        self.ent_login.grid(row=1,column=1,pady=4,padx=4,sticky='we')

        #Campo de senha (mascarado)
        ttk.Label(form, text="Senha: ").grid(row=2,column=0,padx=4,pady=4,sticky='e')
        self.ent_senha = ttk.Entry(form, width=24, show='*')
        self.ent_senha.grid(row=2,column=1,pady=4,padx=4,sticky='we')
        ttk.Label(form,text="deixe em branco para manter a senha atual ao editar"
                  ).grid(row=2, column=2,sticky='w',padx=4, pady=4)
            #dica para edição
        
        #Campo: Perfil (combox somente leitura)
        ttk.Label(form, text="Perfil: ").grid(
                row=3,column=0,padx=4,pady=4)
        #Lista de perfil
        self.cb_perfil = ttk.Combobox(form,values=PERFIS,state='readonly',width=22)
        self.cb_perfil.grid(row=3,column=1,sticky='w',padx=4,pady=4)

        # Barra de botões de ações (CRUD + Utilitários)
        btns = ttk.Frame(self); btns.pack(pady=4)
        
        ttk.Button(btns, text='Salvar',command=self._salvar).grid(row=0,column=0, padx=4)
        ttk.Button(btns, text='Exluir',command=self._excluir).grid(row=0,column=1, padx=4)
        ttk.Button(btns, text='Buscar',command=self._buscar).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text='Limpar',command=self._limpar).grid(row=0, column=3, padx=4)

        #Linha de busca rápida por nome
        quick = ttk.Frame(self.tab_user)
        quick.pack(fill='x',padx=7,pady=(0,4))

        ttk.Label(quick,text="Filtro por Nome: ").pack(side='left',padx=(0,6)) #rotúlo de filtro
        self.ent_busca = ttk.Entry(quick,width=30) #campo de filtro
        self.ent_busca.pack(padx=4, side='left')

        #tk.Button(quick,text="Aplicar", command=self._buscar()).pack(side='left',padx=6)  #aplica o filtro

        # Tabela (TreeView) de usuários
        self.tree_users = ttk.Treeview(self.tab_user,
                                       columns=('id','nome','login','perfil'), #define as colunas de dados
                                       show='headings', #mostrar cabeçalho
                                       height=12 #altura em linhas visiveis
        )

        #Configurar Cabeçalhos e largura da coluna
        for col, txt, wid in (
                                ('id','ID',50), 
                                ('nome','NOME',200),
                                ('login','LOGIN',180),
                                ('pefil','PERFIL',100)
                            ):
                self.tree_users.heading(col,text=txt) #texto do cabeçalho
                self.tree_users.column(col,width=wid, anchor='w') #Largura e alinhamento a esquerda
        
        self.tree_users.pack(fill='both',expand=True) #expande a tabela
                                                                            
    
    def _salvar():
        return
    
    def _excluir():
        return
    
    def _buscar():
        return
    
    def _limpar():
        return












