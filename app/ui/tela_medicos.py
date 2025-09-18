# Tela CRUD de Médicos - usa oi campo "horario_atendimento"  (ex:08:00-17:00)

import tkinter as tk
from tkinter import ttk 
from app.models.medico import Medico

from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medico_repository import MedicoRepository

class TelaMedicos(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.medico_repo = MedicoRepository()
        self.consulta_repo = ConsultaRepository()
        self._build()
        #self._load()

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

        ttk.Button(btns,text="Novo",command=self._novo).grid(row=0,column=0,padx=4)
        ttk.Button(btns,text="Salvar",command=self._salvar).grid(row=0, column=1, padx=4)
        ttk.Button(btns,text="Excluir",command=self._excluir).grid(row=0,column=2,padx=4)
        ttk.Button(btns,text="Buscar",command=self._buscar).grid(row=0, column=3, padx=4)
        ttk.Button(btns,text="Limpar",command=self._limpar).grid(row=0, column=4, padx=4)





