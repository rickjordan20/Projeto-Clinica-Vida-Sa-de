# clinica_vida_saude/app/models/usuario.py
# Modelo de Usuário com construtor explícito
class Usuario:
    def __init__(self, id, nome, login, senha, perfil):
        self.id = id  # Identificador único do usuário
        self.nome = nome  # Nome completo
        self.login = login  # Nome de usuário (para login no sistema)
        self.senha = senha  # Senha em texto ou hash (melhor usar hash na prática)
        self.perfil = perfil  # Perfil: Admin, Recepcionista, Médico
