# clinica_vida_saude/app/ui/tela_consultas.py
import tkinter as tk  #iporta a Biblioteca de Interface Gráfica
from tkinter import ttk, messagebox, filedialog  #Importando dependências da Blioteca do Tkinter
import csv #Importando a Biblioteca CSV para trabalhar com planilhas

from app.models.consulta import Consulta #Importando a Classe Consulta
from app.models.medico import Medico
from app.models.paciente import Paciente
#Importando as conexões do CRUD com o Banco de Dados
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medico_repository import MedicoRepository
from app.repositories.paciente_repository import PacienteRepository

#Importando o o "serviço de agendamento" que contem as regras de negócio
#from app.services.agendamento_service import AgendamentoService, AgendamentoError

#Criação da Tela de Consultas
class TelaConsultas(ttk.Frame):
    def __init__(self, master): #MÉTODO CONSTRUTOR
        super().__init__(master)
        self.consulta_repo = ConsultaRepository() #instanciando a Classe(criar um objeto)
        self.medico_repo = MedicoRepository() #instanciando a Classe(criar um objeto)
        self.paciente_repo = PacienteRepository() #instanciando a Classe(criar um objeto)
        #self.svc = AgendamentoService(self.consulta_repo, self.medico_repo)
        self._build()
        self._fill_combos()
        #self._load()

    def _build(self):
        self.pack(fill='both',expand=True) #RESPOSIVIDADE - adpta ao tamanho da tela
        ttk.Label(self,text="Consultas",font=("Arial",16,"bold")).pack(pady=6)
        
        form = ttk.Frame(self) ; form.pack(padx=8,pady=4,fill="x")

        # COMBOS (usandos para criar consulta e também filtros)
        ttk.Label(form,text="Paciente").grid(row=0,column=0,sticky="e")
        self.cb_paciente = ttk.Combobox(form,width=40,state='readonly')
        self.cb_paciente.grid(row=0,column=1,sticky="we",padx=4,pady=2)

        ttk.Label(form,text="Médico").grid(row=1,column=0,sticky="e")
        self.cb_medico = ttk.Combobox(form,width=40,state='readonly')
        self.cb_medico.grid(row=1,column=1,sticky="we",padx=4,pady=2)

        ttk.Label(form,text="Data (AAAA-MM-DD): ").grid(row=2,column=0,sticky="e")
        self.ent_data = ttk.Entry(form,width=20) ; self.ent_data.grid(row=2,column=1,sticky="w")

        ttk.Label(form,text="Hora (HH:MM): ").grid(row=3,column=0,sticky="e")
        self.ent_hora = ttk.Entry(form,width=20) ; self.ent_hora.grid(row=3,column=1,sticky="w")

        #Linha de filtros(histórico)
        filt = ttk.Frame(self) ; filt.pack(fill="x",padx=8,pady=4)
        
        ttk.Label(filt,text="De(data): ").grid(row=0,column=0,sticky="e")
        self.ent_de = ttk.Entry(filt,width=12) ; self.ent_de.grid(row=0,column=1,padx=4,pady=2)

        ttk.Label(filt,text="Até (data): ").grid(row=0,column=2,sticky="e")
        self.ent_ate = ttk.Entry(filt,width=12) ; self.ent_ate.grid(row=0,column=3,padx=4,pady=2)

        ttk.Label(filt,text="Status: ").grid(row= 0, column=4 ,sticky="e")
        self.cb_status = ttk.Combobox(filt,width=12,state='readonly', values=("Todas","Agendada","Realizada","Cancelada"))
        self.cb_status.grid(row=0,column=5,sticky="w",padx=4,pady=2) #Posicionar o cambo de status
        self.cb_status.set("Todas") #Define um valor PADRÃO de status
        
        #BOTÕES
        btns = ttk.Frame(self) ; btns.pack(pady=4) #Container para os botões de ação
        ttk.Button(btns,text="Agendar",command=self._agendar).grid(row=0,column=0,padx=4)
        ttk.Button(btns,text="Remarcar Selecionada",command=self._remarcar).grid(row=0,column=1,padx=4)
        ttk.Button(btns,text="Cancelar Slecionada",command=self._cancelar).grid(row=0,column=2,padx=4)
        ttk.Button(btns,text="Marcar como Realizada",command=self._concluir).grid(row=0,column=3,padx=4)
        ttk.Button(btns,text="Filtrar (Histórico)",command=self._filtrar).grid(row=0,column=4,padx=4)
        ttk.Button(btns,text="Exportar CSV(Realizadas)",command=self._exportar).grid(row=0,column=5,padx=4)
 
    # Cria a tabela (Treeview) com colunas definidas
        self.tree = ttk.Treeview(self, 
                                columns=('id','pac','med','data','hora','status'), 
                                show='headings', 
                                height=12)

        # Configura cada coluna com cabeçalho, texto e largura
        for col, text, width in (
            ('id','ID',40), 
            ('pac','Paciente',180), 
            ('med','Médico',180), 
            ('data','Data',90), 
            ('hora','Hora',70), 
            ('status','Status',110)
        ):
            # Define o cabeçalho da coluna
            self.tree.heading(col, text=text)
            # Define largura e alinhamento da coluna
            self.tree.column(col, width=width, anchor='w')

        # Adiciona a tabela ao layout
        self.tree.pack(fill='both', expand=True, padx=8, pady=6)

        # Vincula evento de seleção de linha
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        #Cache / estado
        self.map_pac = {} #Nome -> id Dicionário para mapear o nome do paciente para o id
        self.map_med = {} #Nome -> id Dicionário para mapear o nome do médico para o id 
        self.sel_id = None #Guardar o ID da consulta selecioanda
        self.last_items = [] #Última lista exibida (para referência/export)
        #Mantém a última lista mostrada
 

    def _fill_combos(self):
        pacs = self.paciente_repo.find() #Busca todos os pacientes do banco
        meds = self.medico_repo.find() #Busca todos os médicos do banco
        self.map_pac = {p.nome : p.id for p in pacs} #Cria um mapa id->nome para Pacientes
        self.map_med = {m.nome : m.id for m in meds} #Cria um mapa id->nome para Médicos
        self.cb_paciente['values'] = list(self.map_pac.keys()) 
            #Preenche o combo de paciente com os nomes
        self.cb_medico['values'] = list(self.map_med.keys()) 
            #Cria um mapa id->nome para Médicos

    def _load(self, items = None):
        
        self._fill_combos() #Garante os combos sejam atualizados
        if items is None:
            items = self.consulta_repo.find() #Se não veio lista, carrega todas as consultas
        self._last_items = items #carrega o que está na tela e Salva a lista exibida atualmente

        #Limpa e popula a tabela
        for i in self.tree.get_children():
            self.tree.delete(i)
        
      
        #Remove todas as linhas atuais da tabela
        pac_cache = {p.id : p.nome for p in self.paciente_repo.find()}
        #Cache id -> nome de pacientes para exibição
        med_cache = {m.id : m.nome for m in self.medico_repo.find()}
        #Cache id -> nome de medicos para exibição
        for c in items:
            self.tree.insert('','end',values=(
                #Inserir uma linha por consulta
                c.id, #Id da Consulta
                pac_cache.get(c.paciente_id,c.paciente_id), # Mostra o nome do paciente (ou id se faltar)
                med_cache.get(c.medico_id,c.medico_id), # Mostra o nome do  medico (ou is se faltar)
                c.data,c.hora,c.status
            ))
        


    def _on_select(self, _):
        sel = self.tree.selection() # Obtem a seleção atual da tabela
        if not sel: #Se nada for selecionado, sai
            return 
        self.sel_id = int(self.tree.item(sel[0],'values')[0])
            #Salva o ID da consulta selecionada
        
    
    def _agendar(self):
        nome_p = self.cb_paciente.get().strip() 
            #Lê o paciente selecionado
        nome_m = self.cb_medico.get().strip()
            #Lê o médico selecioando
        data = self.ent_data.get().strip()
            #Lê a data informada
        hora = self.ent_hora.get().strip()
            #Lê a hora informada
        
        if not nome_p or not nome_m or not data or not hora:
            messagebox.showwarning("AVISO","Preencha todos os campos corretamente!")
            return
        
        pid = self.map_pac.get(nome_p) #Converte o nome do paciente para id
        mid = self.map_med.get(nome_m) #Converte o nome do médico para id
        
        if pid is None or mid is None:
            messagebox.showerror("ERRO","Seleção de Paciente/Médico inválida!")
            #Falha se o mapeamento não existir 
            
        
        
    def _remarcar(self):

        return
        
    def _cancelar(self):
        
        return 
        
    def _concluir(self):
        
        return 
        
    def _filtrar(self):
        
        return
        
    def _exportar(self):
        
        return

        
    