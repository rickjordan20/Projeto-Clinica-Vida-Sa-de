from typing import Optional #para criar objetos
from app.database.connection import get_connection
from app.models.consulta import Consulta

class ConsultaRepository:
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
