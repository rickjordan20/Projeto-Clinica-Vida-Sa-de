# clinica_vida_saude/app/repositories/paciente_repository.py
# Este arquivo representa o repositório (camada de acesso a dados) para a entidade Paciente.
# Contém as operações CRUD (Create, Read, Update, Delete) utilizando SQLite.

# Importações necessárias
from typing import List, Optional              # Tipagem para indicar listas e valores opcionais
from app.database.connection import get_connection  # Função utilitária que retorna uma conexão com o banco SQLite
from app.models.paciente import Paciente            # Classe modelo que representa um paciente no domínio do sistema

# Classe responsável por manipular os dados da tabela "paciente" no banco de dados
class PacienteRepository:

    def create(self, paciente: Paciente) -> int:
        """
        Cria (insere) um novo paciente no banco de dados.
        Retorna o ID gerado automaticamente para o novo registro.
        """
        conn = get_connection()  # Abre uma conexão com o banco
        try:
            # Executa a instrução SQL de inserção usando placeholders (?) para evitar SQL Injection
            cur = conn.execute(
                "INSERT INTO paciente (nome, cpf, data_nascimento, telefone) VALUES (?,?,?,?)",
                (paciente.nome, paciente.cpf, paciente.data_nascimento, paciente.telefone)
            )
            conn.commit()                # Confirma (grava) as alterações no banco de dados
            return cur.lastrowid         # Retorna o ID do paciente recém-criado
        finally:
            conn.close()                 # Fecha a conexão, garantindo que será fechada mesmo em caso de erro

    def get_by_id(self, id_: int) -> Optional[Paciente]:
        """
        Busca um paciente pelo seu ID.
        Retorna um objeto Paciente se encontrado, ou None se não existir.
        """
        conn = get_connection()
        try:
            # Consulta SQL para buscar um paciente específico pelo ID
            cur = conn.execute(
                "SELECT id, nome, cpf, data_nascimento, telefone FROM paciente WHERE id=?",
                (id_,)  # A vírgula é necessária para criar uma tupla de um único elemento
            )
            row = cur.fetchone()  # Obtém apenas o primeiro resultado (ou None se não existir)
            
            # Retorna um objeto Paciente se encontrar um registro, caso contrário retorna None
            return Paciente(*row) if row else None
        finally:
            conn.close()  # Fecha a conexão ao final

    def find(self, nome: str | None = None, cpf: str | None = None) -> List[Paciente]:
        """
        Lista pacientes aplicando filtros opcionais:
        - nome (busca parcial usando LIKE)
        - cpf (busca exata)
        Retorna uma lista de objetos Paciente.
        """
        conn = get_connection()
        try:
            # SQL base, "WHERE 1=1" facilita adicionar condições dinamicamente
            sql = "SELECT id, nome, cpf, data_nascimento, telefone FROM paciente WHERE 1=1"
            params: list = []  # Lista para armazenar os parâmetros dinamicamente
            
            # Se um nome foi passado, adiciona filtro com LIKE (busca parcial)
            if nome:
                sql += " AND nome LIKE ?"
                params.append(f"%{nome}%")  # "%" permite busca por trecho do nome
            
            # Se um CPF foi passado, adiciona filtro exato
            if cpf:
                sql += " AND cpf = ?"
                params.append(cpf)
            
            # Executa a consulta final com os filtros aplicados
            cur = conn.execute(sql, params)
            
            # Converte cada linha retornada em um objeto Paciente
            return [Paciente(*row) for row in cur.fetchall()]
        finally:
            conn.close()  # Fecha a conexão

    def update(self, paciente: Paciente) -> None:
        """
        Atualiza os dados de um paciente existente no banco.
        É necessário que o paciente tenha um ID válido.
        """
        conn = get_connection()
        try:
            # Comando UPDATE substitui os dados antigos pelos novos com base no ID
            conn.execute(
                "UPDATE paciente SET nome=?, cpf=?, data_nascimento=?, telefone=? WHERE id=?",
                (paciente.nome, paciente.cpf, paciente.data_nascimento, paciente.telefone, paciente.id)
            )
            conn.commit()  # Grava as alterações no banco
        finally:
            conn.close()  # Fecha a conexão

    def delete(self, id_: int) -> None:
        """
        Exclui um paciente do banco de dados com base no ID fornecido.
        """
        conn = get_connection()
        try:
            # Executa a exclusão do registro específico
            conn.execute("DELETE FROM paciente WHERE id=?", (id_,))
            conn.commit()  # Confirma a exclusão
        finally:
            conn.close()  # Fecha a conexão