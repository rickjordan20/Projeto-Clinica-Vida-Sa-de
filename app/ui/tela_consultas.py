# clinica_vida_saude/app/ui/tela_consultas.py
import tkinter as tk  #iporta a Biblioteca de Interface Gráfica
from tkinter import ttk, messagebox, filedialog  #Importando dependências da Blioteca do Tkinter
import csv #Importando a Biblioteca CSV para trabalhar com planilhas

from app.models.consulta import Consulta #Importando a Classe Consulta
#Importando as conexões do CRUD com o Banco de Dados
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medico_repository import MedicoRepository
from app.repositories.paciente_repository import PacienteRepository

#Importando o o "serviço de agendamento" que contem as regras de negócio
from app.services.agendamento_service import AgendamentoService, AgendamentoError

#Criação da Tela de Consultas
class TelaConsultas(ttk.Frame):
    def __init__(self, master): #MÉTODO CONSTRUTOR
        super().__init__(master)
        self.consulta_repo = ConsultaRepository() #instanciando a Classe(criar um objeto)
        self.medico_repo = MedicoRepository() #instanciando a Classe(criar um objeto)
        self.paciente_repo = PacienteRepository() #instanciando a Classe(criar um objeto)
        self.svc = AgendamentoService(self.consulta_repo, self.medico_repo)
        self._build()
        self._load()

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
        self.ent_de = ttk.Entry(filt,width=12) ; self.ent_de.grid(row=0,column=1)

        ttk.Label(filt,text="Até (data): ").grid(row=0,column=2,sticky="e")
        self.ent_ate = ttk.Entry(filt,width=12) ; self.ent_ate.grid(row=0,column=3)





        
    