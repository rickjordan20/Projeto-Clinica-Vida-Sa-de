from typing import Optional, List #para criar objetos
from app.database.connection import get_connection
from app.models.consulta import Consulta

class ConsultaRepository:
    def create(self, c : Consulta):
        conn = get_connection() #conn tem a conexáo com o banco
        try: 
            cursor = conn.execute(""" 
                INSERT INTO consulta(paciente_id, medico_id, data, 
                                  hora, status)
                VALUES(?,?,?,?,?)
             """,c.paciente_id,c.medico_id,c.data,c.hora,c.status)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def get_by_id(self, id_ : int) ->  Optional[Consulta]: #retorna um objeto do tipo Consulta
        conn = get_connection()
        try:
            cursor = conn.execute("""SELECT id,paciente_id,medico_id,data,hora,status 
                                  FROM consulta WHERE id=?""",id_)
            row = cursor.fetchone() #row guarda o resultado do select acima
            return Consulta(*row) if row else None #cria um objeto de Consulta se estiver algo dentro de row
        finally:
            conn.close()
    
    def find(
            self,
            paciente_id : int | None = None,
            medico_id : int | None = None,
            data : str | None = None, 
            status : str | None = None, 
            data_de : str | None = None,
            data_ate : str | None = None,
    ) -> List[Consulta] : #retorna uma lista de objetos criados a partir da classe Consulta
        """Busca consultas por FILTROS OPCIONAIS:
        -paciente_id, medico_id
        -data(exata) ou intervalo (data_de <= data <= data_ate)
        -status
        """
        conn = get_connection()
        try: 
            sql = """SELECT id, paciente_id, medico_id, data, hora, status 
                    FROM consulta WHERE 1=1"""
            params : list = []
            
            if paciente_id:
                sql += " AND paciente_id = ?"
                params.append(paciente_id)

            if medico_id:
                sql += " AND medico_id = ?"
                params.append(medico_id)
            
            if data:
                sql += " AND date(data) = date(?)"
                params.append(data)
            else:
                if data_de:
                    sql += " AND date(data) >= date(?)"
                    params.append(data_de)

                if data_ate:
                    sql += " AND date(data) <= date(?)"
                    params.append(data_ate)
            if status:
                sql = " AND status = ?"
                params.append(status)
            
            sql += " ORDER BY date(data) DESC, time(hora) DESC"
            cursor = conn.execute(sql,params) # guarda o resutado do consulta(sql)
            return[Consulta(*row) for row in cursor.fetchall()]
            #pega cada linha da consulta, guarda dentro de "row" e cria um objeto
        except:
            print("Erro de conexão!")
        finally:
            conn.close()    
    
    def delete(self, id_ : int) -> None:
        conn = get_connection()
        try:
            conn.execute("DELETE FROM consulta WHERE id=?",id_)
            conn.commit()
        finally:
            conn.close()
    
    def update(self, c : Consulta) -> None:
        conn = get_connection()
        try: #se a conexão com o banco der CERTO
            conn.execute("""UPDATE consulta SET paciente_id=?, medico_id=?, data=?, 
                        hora=?,status=? WHERE id=?""",(c.paciente_id,c.medico_id,c.data,c.hora,c.status))
            conn.commit()
        finally:
            conn.close()

    def exists_at(self, medico_id : int, data: str, 
                  hora: str, id_ : int | None = None) -> bool:
        conn = get_connection()
        try:
            #sql - é o nosso codigo BASE(padrão)
            sql = """ 
                SELECT COUNT(1) FROM consulta
                WHERE medico_id=?
                AND date(data) = date(?)
                AND hora = ?
                AND status = "Agendada"
                 """
            #params - é o complemento do codigo sql base
            params = [medico_id,data,hora]
            if id_:
                sql += " AND id <> ?"
                params.append(id_) #adiciona a variavel id_ no final da lista
            cursor = conn.execute(sql,params) # guarda o resultado do sql
            return cursor.fetchone()[0] > 0
        finally:
            conn.close()


    def has_future_for_paciente(self,paciente_id:int)->bool:
        """ Regra de negócio: retorna True se o paciente tiver
         pelo menos 1 consulta com o status Agendada no futuro """
        conn = get_connection()
        try:
            sql = """
                    SELECT COUNT(1) FROM consulta WHERE 
                    paciente_id=? AND status="Agendada"
                    AND datatime(data || '' || hora) > datatime('now')
                """
            cursor = conn.execute(sql,(paciente_id,))
            return cursor.fetchone()[0]>0 #retorna a consulta SQL na primeira 
                                           # linha quando for maior que zero
        finally:
            conn.close()   

    def has_future_for_medico(self,medico_id:int)->bool:
        """Regra de Negócio: Retorna True se o médico estiver com uma consulta
            com status de "Agendada" no futuro """
        
        conn = get_connection()
        try:
            sql = """" SELECT COUNT(1) FROM consulta
                    WHERE medico_id=?
                    AND status ="Agendada"
                    AND datatime(data || '' || hora) > datatime('now')"""
            cursor = conn.execute(sql,(medico_id,))
            return cursor.fetchone()[0]>0
        finally:
            conn.close()
