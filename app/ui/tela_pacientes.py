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
        self.repo = PacienteRepository()         # acesso ao CRUD de pacientes
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