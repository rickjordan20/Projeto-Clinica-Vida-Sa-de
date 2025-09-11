
# clinica_vida_saude/app/models/medico.py
# Modelo de Médico com construtor explícito
class Medico:
    def __init__(self, id, nome, crm, especialidade, horario_atendimento):
        self.id = id  # Identificador único no banco
        self.nome = nome  # Nome completo do médico
        self.crm = crm  # CRM (deve ser único)
        self.especialidade = especialidade  # Área de atuação do médico
        self.horario_atendimento = horario_atendimento  # Faixa de horários disponíveis
