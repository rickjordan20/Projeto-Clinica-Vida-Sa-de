#Tela Administrativa - Abas: (1) Usuários(crud) (2)Backup/Restore 

import tkinter as tk
from tkinter import ttk,messagebox,filedialog 
#Widgets ttk e diálogos padrão(caixa de mensagem,abrir aquivo)

import sqlite3 #Para captura erros de integridade 

from app.repositories.usuario_repository import UsuarioRepository
from app.services.backup_service import BackupService
from app.models.usuario import Usuario

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
        self.bkp = BackupService()
        self.sel_user_id = None
        #Guarda o ID do usuário selecionado na tabela (None=nenhum)
        self._build() # Monta toda a iterface(abas, forms, botões,etc.)
        self._user_load() # Carrega os usuários do banco e preenche o TreeView

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
        
        ttk.Button(btns, text='Salvar',command=self._user_salvar).grid(row=0,column=0, padx=4)
        ttk.Button(btns, text='Exluir',command=self._user_excluir).grid(row=0,column=1, padx=4)
        ttk.Button(btns, text='Buscar',command=self._user_buscar).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text='Limpar',command=self._user_limpar).grid(row=0, column=3, padx=4)

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
                                ('perfil','PERFIL',100)
                            ):
                self.tree_users.heading(col,text=txt) #texto do cabeçalho
                self.tree_users.column(col,width=wid, anchor='w') #Largura e alinhamento a esquerda
        
        self.tree_users.pack(fill='both',expand=True) #expande a tabela

        #Vincula o evento de seleção de linha a rotina que preenche 
        # o formulário com os dados selecionados
        self.tree_users.bind('<<TreeviewSelect>>',self._user_on_select)

    def _user_load(self, items = None):
        """ Carrega/recarrega a tabela com os usuários fornecidos (ou todos, se None)"""
        #Limpar todos os itens atuais de TreeView(tabela)
        for i in self.tree_users.get_children():
            self.tree_users.delete(i)

        # Se não recebeu uma linha filtrada, busca todos no repositório
        items = items or self.repo_user.find()

        #Insere cada usuário com uma linha na TreeView
        for u in items:
            self.tree_users.insert('','end',
                                   values=(u.id,u.nome,u.login, u.perfil))
    
    def _user_on_select(self,_):
        ''' Handler disparado ao selecionar uma linha na tabela:
            preenche o formulário'''
        
        sel = self.tree_users.selection() 
            # Obtem os itens selecionados
        if not sel:
            return #Nada selecionado > sai 
        
        vals = self.tree_users.item(sel[0],'values') 
            #Recupera a teuplade valores da linha
        self.sel_user_id = int(vals[0]) 
            #Guarda o ID selecionado para operações futuras
        

        u = self.repo_user.get_by_id(self.sel_user_id)
            #Busca o u suário completo pelo ID (do banco

        if not u:
            return
        
        #Preenche o formulário (não exibe a senha por segurança)
        self.ent_nome.delete(0,tk.END); self.ent_nome.insert(0,u.nome)
        self.ent_login.delete(0,tk.END); self.ent_login.insert(0,u.login)
        self.ent_senha.delete(0,tk.END)

        self.cb_perfil.set(u.perfil or "Recepcionista")
            #Defgine o perfil atual (ou padrão)

    def _user_novo(self):
        #Prepara o formulário para inserir um usuário novo
        self.sel_user_id = None # None indica o modo de criação (create)
        self._user_limpar () #Limpa os campos e filtro
    
    def _user_limpar(self):
        # Limpa os campos do fomrulário e o campo de busca
        for ent in (self.ent_nome,self.ent_login, self.ent_senha):
            ent.delete(0,tk.END) #Limpa cada campo Entry
        
        self.cb_perfil.set("Recepcionista") 
            # Restaurar o valor padrão do perfil
        self.ent_busca.delete(0,tk.END) #Limpa o filtro de busca
    
    def _user_salvar(self):
        """Insere (CREATE) ou atualiza(UPDATE)
          um usuário, conforme o estado atual"""
        nome = self.ent_nome.get().strip()
        login = self.ent_login.get().strip()
        senha = self.ent_senha.get().strip()
        perfil = self.cb_perfil.get().strip() or "Recepcionista"

        if not nome or not login:
            messagebox.showwarning("Aviso", "Nome e Login são obrigatórios!")
            return
        
        try:
            if self.sel_user_id is None:
                #Modo INSERT(novo registro): exige senha informada
                if not senha:
                    messagebox.showwarning("Aviso",
                                              "Informe uma senha para o usuário")
                    return
                #Monta o modelo de dominio(usuário)
                u = Usuario(
                    id = self.sel_user_id,
                    nome=nome,
                    login=login,
                    senha=senha,
                    perfil=perfil
                )
                self.repo_user.update(u)
            else:
                #Modo UPDATE: se a senha não for informada, mantem a senha atual do banco
                atual = self.repo_user.get_by_id(self.sel_user_id) # contem o usuário atual logado
                if not atual:
                    messagebox.showerror("Erro","Usuário não encontrado!")
                    return
                senha_final = senha if senha else atual.senha # Mantém a senha antiga do banco de dados
                u = Usuario(
                    id = self.sel_user_id,
                    nome=nome,
                    login=login,
                    senha=senha,
                    perfil=perfil
                )
                self.repo_user.update(u) # atualiza no banco

                # Recarrega a tabela para refletir as alterações feitas
                self._user_load()
                messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")
        
        except sqlite3.IntegrityError:
            # Erro de Integridade para garantir a conscistência dos dados
            messagebox.showerror("Erro","Login já existente! Escolha outro.")

        except Exception as e:
            messagebox.showerror("Erro",str(e))

    def _user_excluir(self):
        #Exclui o usuário selecionado após confirmação
        if self.sel_user_id is None:
            return # Ninguém selecionado  - nada a fazer
        # Confirmação de ação destruir
        if not messagebox.askyesno("Confirmar","Deseja excluir este usuário?"):
            return
        try:
            self.repo_user.delete(self.sel_user_id) # Remove do banco
            self.sel_user_id = None #Limpa a seleção atual
            self._user_limpar() #Limpa o formulário
            self._user_load() #Recarrega a grade
        except Exception as a:
            messagebox.showerror("Erro",str(a))     #Exibe erros inesperados       

        
    def _user_buscar(self):
        # Filtra os usuários pelo nome e recarrega a tabela com o resultado
        nome = self.ent_busca.get().strip() or None # None pode significar "sem filtro"
        items = self.repo_user.find(nome=nome) # Busca filtrada no repositório
        if not items:
            messagebox.showinfo("Info", "Nenhum usuário encontrado!")
        
        self._user_load(items) #Recarrega a tabela com a listra (mesmo vazia)
    
    #-----------------------------Aba: Backup e Restore----------------------------
    def _build_backup_tab(self):
        #Monta a aba de backup e restauração de banco
        wrap = ttk.Frame(self.tab_backup)
        wrap.pack(fill='x',expand=True,padx=8,pady=8)
        ttk.Label(wrap,text="Backup e Restauração do Banco",
                  font=("Arial",14,"bold")).pack(pady=(0,8))
        
        #Botões de ação(backup e restore)
        btns = ttk.Frame(wrap)
        btns.pack(pady=8)
        ttk.Button(btns,text="Gerar Backup",
                   command=self._backup).grid(row=0,column=0, padx=6)
        
        ttk.Button(btns,text="Restaurar Backup",
                   command=self._restore).grid(row=0,column=1, padx=6)
        
        """Aviso de boa prática: reinicializar o app após restore 
        evita conexão com o Banco"""
        ttk.Label(wrap, 
                  text="Após restaurar, reinicie o sistema!",
                 foreground='#555555' ).pack(pady=6)
    
    def _backup(self):
        # Gera um arquivo de backup do banco atual e informa o caminho
        try:
            path = self.bkp.backup() #Caminho do backup
            messagebox.showinfo("Sucesso",f"Backup criado em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro",str(e))

    def _restore(self):
        """Restaura o banco a partir de um arquivo .db escolhido pelo usuário."""
        # Abre seletor de arquivos, filtrando preferencialmente .db
        file = filedialog.askopenfilename(
            title='Selecione o arquivo de backup',
            filetypes=[('DB','*.db'),('Todos','*.*')]
        )
        if not file:
            return  # Usuário cancelou a seleção
        # Confirmação antes de uma operação potencialmente destrutiva (sobrescrever o banco atual)
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja restaurar este backup?"):
            return
        try:
            self.bkp.restore(file)                                        # Delegado ao serviço de backup
            messagebox.showinfo('Sucesso','Backup restaurado. Reinicie o sistema.')
        except Exception as e:
            messagebox.showerror('Erro', str(e))                          # Exibe qualquer falha no processo





        
        

        



    












