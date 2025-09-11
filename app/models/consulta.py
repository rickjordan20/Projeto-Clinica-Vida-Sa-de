# clinica_vida_saude/app/models/consulta.py
# Modelo de Consulta com construtor explícito
class Consulta:
    def __init__(self, id, paciente_id, medico_id, data, hora, status):
        self.id = id  # Identificador único da consulta
        self.paciente_id = paciente_id  # FK para paciente.id
        self.medico_id = medico_id  # FK para medico.id
        self.data = data  # Data da consulta (YYYY-MM-DD)
        self.hora = hora  # Horário da consulta (HH:MM)
        self.status = status  # Agendada, Realizada, Cancelada
