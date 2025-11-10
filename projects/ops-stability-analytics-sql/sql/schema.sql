-- Esquema base: agentes, equipos, calendario y hechos/semi-agregados
CREATE SCHEMA IF NOT EXISTS ops;

CREATE TABLE IF NOT EXISTS ops.team (
  team_id   text PRIMARY KEY,
  team_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS ops.agent (
  agent_id  text PRIMARY KEY,
  team_id   text NOT NULL REFERENCES ops.team(team_id),
  hire_date date
);

CREATE TABLE IF NOT EXISTS ops.calendar (
  dt        date PRIMARY KEY,
  iso_week  int  NOT NULL,
  iso_year  int  NOT NULL
);

-- Hechos semanales (derivados del pipeline)
CREATE TABLE IF NOT EXISTS ops.weekly_perf (
  agent_id       text NOT NULL REFERENCES ops.agent(agent_id),
  team_id        text NOT NULL REFERENCES ops.team(team_id),
  iso_week       int  NOT NULL,
  iso_year       int  NOT NULL,
  hours_mean     numeric,
  cases_mean     numeric,
  out_hours_flag int,
  out_cases_flag int,
  PRIMARY KEY (agent_id, iso_year, iso_week)
);

-- Agregados por agente (stability)
CREATE TABLE IF NOT EXISTS ops.agent_stability (
  agent_id            text NOT NULL REFERENCES ops.agent(agent_id),
  team_id             text NOT NULL REFERENCES ops.team(team_id),
  cv_hours            numeric,
  cvm_hours           numeric,
  cv_cases            numeric,
  cvm_cases           numeric,
  quartile_efficiency int,
  PRIMARY KEY (agent_id)
);