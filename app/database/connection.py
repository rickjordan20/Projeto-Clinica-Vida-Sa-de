# clinica_vida_saude/app/database/connection.py
# Este módulo centraliza:
# 1) Como abrir conexão com o SQLite (get_connection)
# 2) Como criar/verificar as tabelas a partir do schema.sql (init_db)
# 3) Um "seed" didático: cria o usuário admin/admin123 se não houver usuários


import sqlite3                 # Driver SQLite embutido no Python (não precisa instalar)
from pathlib import Path       # Path ajuda a achar o arquivo schema.sql de forma portátil


DB_PATH = "clinica.db"         # Nome do arquivo do banco (ficará na raiz do projeto)
SCHEMA_FILE = Path(__file__).with_name("schema.sql")  # Aponta para app/database/schema.sql


def get_connection():
    """Abre uma conexão SQLite e liga as chaves estrangeiras."""
    conn = sqlite3.connect(DB_PATH)          # Abre (ou cria) o arquivo .db
    conn.execute("PRAGMA foreign_keys = ON") # Liga integridade referencial (FKs) no SQLite
    return conn                              # Devolve a conexão para os repositórios/services


def init_db():
    """Executa o schema.sql (cria tabelas/índices) e faz seed do usuário admin, se necessário."""
    # Usamos "with" para fechar a conexão automaticamente ao final (mesmo se ocorrer exceção)
    with get_connection() as conn:
        # Abre o arquivo de schema (UTF-8 para aceitar acentos nos comentários)
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            sql = f.read()                   # Lê todo o conteúdo do schema.sql
            conn.executescript(sql)          # Executa vários comandos SQL de uma vez


        # ----------------- SEED DIDÁTICO -----------------
        # Verifica se a tabela 'usuario' está vazia
        cur = conn.execute("SELECT COUNT(1) FROM usuario")
        qtd = cur.fetchone()[0]              # Pega a contagem (ex.: 0 se não há linhas)
        if qtd == 0:                         # Se não existe nenhum usuário ainda...
            # Cria um usuário administrador padrão para facilitar o primeiro login
            conn.execute(
                "INSERT INTO usuario (nome, login, senha, perfil) VALUES (?,?,?,?)",
                ("Administrador", "admin", "admin123", "Admin")
            )
            conn.commit()                    # Garante que o INSERT seja salvo no .db
