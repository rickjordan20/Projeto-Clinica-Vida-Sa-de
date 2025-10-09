from models.usuario import Usuario #importa a classe
from database.connection import get_connection
from typing import Optional, List #trabalhar com classes e objetos

class UsuarioRepository:
    #CREATE, READ, UPDATE, DELETE

    def create(self, u: Usuario):
        # Insere um novo usuário e retorna o ID
        conn = get_connection() #guarda a conexão com o BD
        try:
            cursor = conn.execute(
                """INSERT INTO usuario (nome,login,senha,perfil)
                   VALUES (?,?,?,?)""",(u.nome,u.login,u.senha,u.perfil)
            )
            conn.commit() #Salva as alterações no BD
            return cursor.lastrowid
        finally:
            conn.close() # Fecha a conexão
    
    def get_by_id(self,id_:int) -> Optional[Usuario]:
        #Busca o usuário por ID
        conn = get_connection()
        try:
            cursor = conn.execute(
                """SELECT id, nome, login, senha, perfil FROM usuario
                  WHERE id=?""",(id_)
            )
            row = cursor.fetchone #guarda uma tupla com o resultado do select
            return Usuario(*row)
        finally:
            conn.close()

    def get_by_login(self,login:str) -> Optional[Usuario]:
        #Busca usuário por logio (para autenticação)
        conn = get_connection()
        try:
            cursor = conn.execute(
                """SELECT id,nome,login,senha,perfil FROM usuario 
                WHERE login=?""",(login)
            )
            row = cursor.fetchone()
            return Usuario(*row) if row else None
        finally:
            conn.close()
    
    def find(self, nome: str | None = None,
              perfil:str | None = None) -> List[Usuario]:
        # Listar os usuários por filtros opcionais
        #               (nome LIKE, perfil exato)
        conn = get_connection()
        try: 
            sql = "SELECT id, nome, senha, perfil FROM usuario WHERE 1=1"
            params : List = [] #declara e cria uma lista vazia

            if nome:
                sql += " AND nome LIKE ?"
                params.append(f"%{nome}%")
            if perfil:
                sql += "AND perfil LIKE ?"
                params.append(perfil)
            cursor = conn.execute(sql,params)
            row = cursor.fetchone() # guarda o resultado do Select
            return  [Usuario(*row) if row else None]
        finally:
            conn.close()

    def update(self, u: Usuario):
        # Atualiza usuários existente
        conn = get_connection()
        try:
            conn.execute("""UPDATE usuario SET nome=?,login=?,
                         senha=?,perfil=? WHERE id=?""",
                         u.nome,u.login,u.senha,u.perfil,u.id)
            conn.commit() 
        finally:
            conn.close
    
    def delete(self,id_:int) -> None:
        # Exclui o usuario pelo ID
        conn = get_connection()
        try:
            conn.execute("DELETE FROM usuario WHERE id=?",(id_))
            conn.commit()
        finally:
            conn.close()
