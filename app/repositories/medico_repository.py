from typing import List,Optional 
#Esses tipos são usados para indicar apenas o que a função retorna ou recebe
# List[Medico] -> Indica que a função retorna uma lista contendo objetos do tipo Medico
# Optional[Medico] -> Indica que a função pode retornar um ojeto Medico 
#                                           ou None(quando não encontrar nada
from app.database.connection import get_connection # Função que conecta com o banco
from app.models.medico import Medico #Classe que representa um Medico

class MedicoRepository: 
    #Classe reponsável por acessar e manipular dados da tabela Medico
    def create(self, medico : Medico) -> int: # Cria um novo medico e retorna o ID gerado
        conn = get_connection() #abre uma conexão com o banco
        try:
            cur = conn.execute(""" INSERT INTO medico(nome,crm,especialidade,horario_atendimento)
                                      VALUES(?,?,?,?)""",
                                        (medico.nome,medico.crm,medico.especialidade,medico.horario_atendimento))
            #Preenche os "?" com os dados do objeto
            conn.commit() # Confirma e salva as alteracoes no banco
            return cur.lastrowid #Retorna o ID gerado automaticamente pelo banco
        except:
            print("erro de conexão")
        finally:
            conn.close() # Fecha a conexão com o banco, mesmo que tenha erro
    
    def get_by_id(self, id_ : int) -> Optional[Medico]:
        # Busca um medico pelo ID
        # Pode retornar:
        # - Um objeto Medico, se o registro for encontrado
        # - None, se não encontrar nada (por isso Optional[Medico])
        conn = get_connection() # Abre a conexão
        try:
            cursor = conn.execute("""
                                    SELECT id, nome, crm, especialidade,horario_atendimento
                                    FROM medico WHERE id=?          
                               """,(id_,)) # o parametro deve ser passado como tupla, mesmo que tenha um so valor
            row = cursor.fetchone() # Retorna apenas uma linha do resultado
            return Medico(*row) if row else None #cria um objeto de forma dinamica
            #Se encontrou algo, cria um objeto Medico com os valores da linha do select usando *
        except:
            print("Erro de conexão")
        finally:
            conn.close() # fecha a conexão com o banco
    
    def find(self, nome : str | None = None, crm : str |
              None = None, especialidade : str | None=None) -> List[Medico]:
        # Lista medicos aplicando filtros OPCIONAIS
        # Pode filtrar por:
        # - nome (busca parcial com LIKE)
        # - crm (busca exata)
        # - especialidade (busca parcial com LIKE)
        # Retorna SEMPRE uma lista, que pode estar vazia   
         conn = get_connection() # Abre a conexão
         try: # Base da query. "WHERE 1=1" facilita adicioanr condições depois
             sql = "SELECT id,nome,crm,especialidade,horario_atendimento FROM medicos WHERE 1=1"
             params = list = [] #Lista que armazena valores para os filtros (seguindo a ordem dos ?)

             if nome: # Se o filtro "nome" foi preenchida  
                 sql += " AND nome LIKE ?" 
                 params.append(f"%{nome}%") # Usa "%" para buscar nomes parecidos

             if crm: # Se o filtro crm foi preenchido
                 sql += " AND crm = ?"
                 params.append(crm)

             if especialidade: # Se o filtro especialidade foi preenchido
                 sql += " AND especialidade LIKE ?"
                 params.append(f"%{especialidade}%") # Usa "%" para buscar nomes parecidos
            
             cursor = conn.execute(sql,params)

             return [Medico(*row) for row in cursor.fetchall()] #Retorna uma lista de objetos do tipo Médico
                    #Para cada linha retornada pelo banco, cria um objeto Medico
                    #Retorna todos dentro de uma lista
         finally:
             conn.close() # Fecha a conexão
    
    def update (self, medico : Medico) -> None :
        #Atualiza os dados de um médico existente no banco
        conn = get_connection() #abre a conexão
        try:
            conn.execute("""UPDATE medico SET nome=?, crm=?, 
                         especialidade=?,horario_atendimento=? WHERE id=?""",
                         (medico.nome,medico.crm,medico.especialidade,medico.horario_atendimento))
                          #O WHERE garante que so sera alteradoo registro correto
            conn.commit() #salva as alteracoes o banco
        finally:
            conn.close() #fecha a conexáo
    
    def delete(self, id_:int):
        conn = get_connection()
        try:
            conn.execute("DELETE FROM medico WHERE id=?",(id_))
            #Executa o comando delete de forma segura
            conn.commit() # confirma a eclusao
        finally:
            conn.close() #Fecha a conexao

        




        

                        