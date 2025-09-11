# clinica_vida_saude/app/ui/tela_consultas.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

from app.models.consulta import Consulta
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medico_repository import MedicoRepository
from app.repositories.paciente_repository import PacienteRepository
from app.services.agendamento_service import AgendamentoService, AgendamentoError

class TelaConsultas(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.consulta_repo = ConsultaRepository()
        self.medico_repo = MedicoRepository()
        self.paciente_repo = PacienteRepository()
        self.svc = AgendamentoService(self.consulta_repo, self.medico_repo)

        self._build()
        self._load()