-- clinica_vida_saude/app/database/schema.sql
-- Este arquivo define a estrutura do banco (tabelas, chaves, índices)
-- Formatos de data/hora adotados (TEXT no SQLite):
--   data  = 'YYYY-MM-DD' (ex.: '2025-09-08')
--   hora  = 'HH:MM'      (ex.: '14:30', preferindo múltiplos de 15 min)

-- Ativa verificação de chaves estrangeiras no nível do banco
-- (Também ativamos no Python via PRAGMA em get_connection; manter aqui é saudável)
PRAGMA foreign_keys = ON;

------------------------------------------------------------
-- TABELA: paciente
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paciente (
  id               INTEGER PRIMARY KEY AUTOINCREMENT, -- PK numérica auto-incrementada
  nome             TEXT    NOT NULL,                  -- Nome completo do paciente
  cpf              TEXT    NOT NULL UNIQUE,           -- CPF único (regra de negócio RB01)
  data_nascimento  TEXT,                              -- Data de nascimento (YYYY-MM-DD)
  telefone         TEXT                               -- Telefone (opcional)
);

------------------------------------------------------------
-- TABELA: medico
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS medico (
  id                   INTEGER PRIMARY KEY AUTOINCREMENT, -- PK numérica auto-incrementada
  nome                 TEXT    NOT NULL,                  -- Nome completo do médico
  crm                  TEXT    NOT NULL UNIQUE,           -- CRM único (regra de negócio RB02)
  especialidade        TEXT,                              -- Ex.: "Clínico Geral"
  horario_atendimento  TEXT                               -- Janela do dia, ex.: '08:00-17:00'
);

------------------------------------------------------------
-- TABELA: consulta
-- Armazena um agendamento pontual (data + hora).
-- Regras aplicadas no Service:
--  - Hora em múltiplos de 15min; não pode ser no passado
--  - Deve estar dentro do horário do médico
--  - Não pode haver conflito para o mesmo médico, data e hora
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS consulta (
  id          INTEGER PRIMARY KEY AUTOINCREMENT, -- PK numérica auto-incrementada
  paciente_id INTEGER NOT NULL,                  -- FK para paciente.id (quem será atendido)
  medico_id   INTEGER NOT NULL,                  -- FK para medico.id (quem atende)
  data        TEXT    NOT NULL,                  -- 'YYYY-MM-DD' (dia do atendimento)
  hora        TEXT    NOT NULL,                  -- 'HH:MM' (horário do atendimento)
  status      TEXT    NOT NULL DEFAULT 'Agendada', -- 'Agendada' | 'Realizada' | 'Cancelada'

  -- Define chaves estrangeiras e comportamento de exclusão:
  -- ON DELETE RESTRICT impede apagar paciente/médico se houver consultas associadas,
  -- preservando o histórico e a integridade do agendamento.
  FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE RESTRICT,
  FOREIGN KEY (medico_id)   REFERENCES medico(id)   ON DELETE RESTRICT,

  -- Garante no nível do banco: não existe 2 consultas para o MESMO médico
  -- na MESMA data e MESMA hora (evita conflito de agenda).
  UNIQUE (medico_id, data, hora)
);

------------------------------------------------------------
-- TABELA: usuario
-- Tabela didática para autenticação (senha em texto; em produção use HASH).
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
  id     INTEGER PRIMARY KEY AUTOINCREMENT, -- PK numérica
  nome   TEXT NOT NULL,                     -- Nome do usuário
  login  TEXT NOT NULL UNIQUE,              -- Login único (evita duplicidade)
  senha  TEXT NOT NULL,                     -- SENHA EM TEXTO (apenas didático!)
  perfil TEXT                               -- 'Admin' | 'Recepcionista' | 'Medico'
);

------------------------------------------------------------
-- ÍNDICES (melhoram performance nas consultas mais comuns)
------------------------------------------------------------

-- Consultas por médico e por data/hora (listagens e checagem de conflito)
CREATE INDEX IF NOT EXISTS idx_consulta_medico_datahora
  ON consulta (medico_id, data, hora);

-- Consultas por paciente (histórico do paciente)
CREATE INDEX IF NOT EXISTS idx_consulta_paciente
  ON consulta (paciente_id);

-- Consultas por data (relatórios/filtragem por período)
CREATE INDEX IF NOT EXISTS idx_consulta_data
  ON consulta (data);
