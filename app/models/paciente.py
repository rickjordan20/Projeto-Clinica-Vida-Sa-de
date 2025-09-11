# clinica_vida_saude/app/models/paciente.py
# Modelo de Paciente com construtor explícito
class Paciente:
    def __init__(self, id, nome, cpf, data_nascimento, telefone):
        self.id = id  # Identificador único no banco
        self.nome = nome  # Nome completo do paciente
        self.cpf = cpf  # CPF (deve ser único)
        self.data_nascimento = data_nascimento  # Data de nascimento (YYYY-MM-DD)
        self.telefone = telefone  # Telefone de contato
