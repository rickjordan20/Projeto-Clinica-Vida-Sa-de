# clinica_vida_saude/app/services/agendamento_service.py
# Serviço responsável pelas regras de negócio do agendamento de consultas


from datetime import datetime
from app.models.consulta import Consulta
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medico_repository import MedicoRepository


class AgendamentoError(Exception):
    """Erro personalizado para violação de regras de negócio no agendamento."""
    pass


class AgendamentoService:
    def __init__(self, consulta_repo: ConsultaRepository, medico_repo: MedicoRepository):
        self.consulta_repo = consulta_repo
        self.medico_repo = medico_repo


    # ---------------- Validações principais ----------------


    @staticmethod
    def _validar_hora_15min(hora: str) -> bool:
        """Valida se a hora está no formato HH:MM e é múltiplo de 15 minutos."""
        try:
            h, m = map(int, hora.split(':'))
            return 0 <= h < 24 and 0 <= m < 60 and (m % 15 == 0)
        except Exception:
            return False


    @staticmethod
    def _is_past(date_str: str, time_str: str) -> bool:
        """Retorna True se a data/hora informada já passou."""
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            return dt < datetime.now()
        except Exception:
            return True  # se não parsear, trata como inválido


    def validar(self, c: Consulta, ignore_id: int | None = None) -> None:
        """Executa TODAS as validações de regras de negócio."""


        # 1) Campos obrigatórios
        if not c.paciente_id or not c.medico_id or not c.data or not c.hora:
            raise AgendamentoError("Paciente, Médico, Data e Hora são obrigatórios.")


        # 2) Hora deve ser múltiplo de 15 minutos
        if not self._validar_hora_15min(c.hora):
            raise AgendamentoError("Hora deve ser múltiplo de 15 minutos (ex.: 08:00, 08:15).")


        # 3) Data/hora não pode estar no passado
        if self._is_past(c.data, c.hora):
            raise AgendamentoError("Não é permitido agendar no passado.")


        # 4) Médico deve existir
        medico = self.medico_repo.get_by_id(c.medico_id)
        if not medico:
            raise AgendamentoError("Médico não encontrado.")


        # 5) Horário deve estar dentro do expediente do médico
        if medico.horario_atendimento:
            try:
                inicio_str, fim_str = medico.horario_atendimento.split('-')
                inicio = datetime.strptime(inicio_str, "%H:%M").time()
                fim = datetime.strptime(fim_str, "%H:%M").time()
                hora_consulta = datetime.strptime(c.hora, "%H:%M").time()
                if not (inicio <= hora_consulta <= fim):
                    raise AgendamentoError("Consulta fora do horário de atendimento do médico.")
            except Exception:
                raise AgendamentoError("Formato de horário do médico inválido. Use HH:MM-HH:MM.")


        # 6) Não pode existir outra consulta no mesmo dia/hora para o mesmo médico
        if self.consulta_repo.exists_at(c.medico_id, c.data, c.hora, ignore_id=ignore_id):
            raise AgendamentoError("Conflito: o médico já possui consulta neste horário.")


    # ---------------- Ações ----------------


    def agendar(self, c: Consulta) -> int:
        """Cria nova consulta após validar todas as regras."""
        self.validar(c)
        return self.consulta_repo.create(c)


    def remarcar(self, c: Consulta) -> None:
        """Atualiza data/hora de uma consulta existente."""
        self.validar(c, ignore_id=c.id)
        self.consulta_repo.update(c)


    def cancelar(self, consulta_id: int) -> None:
        """Marca uma consulta como Cancelada."""
        consulta = self.consulta_repo.get_by_id(consulta_id)
        if not consulta:
            raise AgendamentoError("Consulta não encontrada.")
        if consulta.status == "Realizada":
            raise AgendamentoError("Não é possível cancelar uma consulta já realizada.")
        consulta.status = "Cancelada"
        self.consulta_repo.update(consulta)


    def concluir(self, consulta_id: int) -> None:
        """Marca uma consulta como Realizada."""
        consulta = self.consulta_repo.get_by_id(consulta_id)
        if not consulta:
            raise AgendamentoError("Consulta não encontrada.")
        consulta.status = "Realizada"
        self.consulta_repo.update(consulta)
