# ===============================================================
# app/services/backup_service.py
# ---------------------------------------------------------------
# OBJETIVO:
# Este arquivo cria uma CLASSE responsável por fazer:
#   1️ Backup (cópia de segurança do banco de dados SQLite)
#   2️ Restauração (recuperar o banco a partir de um backup)
# ---------------------------------------------------------------
# Ele pertence à camada de "SERVIÇOS" do projeto, ou seja,
# contém regras e operações que não são diretamente interface
# (Tkinter) nem banco de dados (SQL), mas sim um serviço de apoio.
# ===============================================================


import os          # Biblioteca padrão do Python para manipular arquivos e diretórios
import shutil      # Fornece funções para copiar, mover ou deletar arquivos
from datetime import datetime  # Usada para gerar data e hora no nome do backup


# ===============================================================
# CLASSE: BackupService
# ---------------------------------------------------------------
# Essa classe centraliza as operações de BACKUP e RESTAURAÇÃO
# do banco de dados principal (ex.: clinica.db).
# ===============================================================
class BackupService:


    # -----------------------------------------------------------
    # MÉTODO CONSTRUTOR (__init__)
    # -----------------------------------------------------------
    # É executado automaticamente ao criar um objeto da classe.
    # Define o caminho do banco de dados e a pasta onde os backups
    # serão armazenados.
    # -----------------------------------------------------------
    def __init__(self, db_path='clinica.db', backup_dir='backups'):
        self.db_path = db_path            # Caminho do arquivo do banco (.db) que será copiado
        self.backup_dir = backup_dir      # Diretório onde ficarão salvos os backups


        # Cria a pasta de backup caso ela não exista ainda.
        # 'exist_ok=True' impede erro se a pasta já existir.
        os.makedirs(self.backup_dir, exist_ok=True)


    # -----------------------------------------------------------
    # MÉTODO: backup()
    # -----------------------------------------------------------
    # Cria uma cópia do banco de dados atual dentro da pasta
    # de backups, com um nome que inclui a data e hora do momento.
    # -----------------------------------------------------------
    def backup(self) -> str:
        """Cria uma cópia do banco atual com timestamp no nome."""


        # Verifica se o arquivo do banco realmente existe antes de tentar copiar.
        if not os.path.exists(self.db_path):
            # Caso o banco não exista, dispara um erro informando ao usuário.
            raise FileNotFoundError("Arquivo de banco de dados não encontrado.")


        # Gera um carimbo de data/hora (timestamp) no formato:
        # AAAAMMDD_HHMMSS — exemplo: 20251009_101530
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


        # Monta o caminho completo do arquivo de backup que será criado:
        # Exemplo: backups/backup_20251009_101530.db
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.db")


        # Usa 'shutil.copy2' para copiar o banco.
        # copy2 preserva metadados como data de criação/modificação.
        shutil.copy2(self.db_path, backup_file)


        # Retorna o caminho completo do backup criado, útil para exibir na interface.
        return backup_file


    # -----------------------------------------------------------
    # MÉTODO: restore()
    # -----------------------------------------------------------
    # Substitui o banco atual por um arquivo de backup escolhido.
    # Deve ser usado com cuidado, pois apaga os dados recentes.
    # -----------------------------------------------------------
    def restore(self, backup_file: str) -> None:
        """Substitui o banco atual por um arquivo de backup."""


        # Verifica se o arquivo de backup realmente existe.
        if not os.path.exists(backup_file):
            # Se não existir, gera um erro explicativo.
            raise FileNotFoundError("Arquivo de backup não encontrado.")


        # Copia o arquivo de backup para o local do banco original,
        # sobrescrevendo o banco atual.
        shutil.copy2(backup_file, self.db_path)


        # Importante:
        # Depois de restaurar, é recomendado reiniciar o sistema,
        # pois o programa pode manter conexões antigas abertas com o banco antigo.
