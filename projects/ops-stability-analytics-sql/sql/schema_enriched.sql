CREATE SCHEMA IF NOT EXISTS ops;

-- Tablas sintéticas enriquecidas
CREATE TABLE IF NOT EXISTS ops.synthetic_team (
  team_id   text PRIMARY KEY,
  team_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS ops.synthetic_agent (
  agent_id       text PRIMARY KEY,
  team_id        text NOT NULL,
  role           text NOT NULL,
  monthly_salary numeric NOT NULL,
  hourly_cost    numeric NOT NULL,
  hire_date      date NOT NULL
);

CREATE TABLE IF NOT EXISTS ops.synthetic_case_pricing (
  case_type     text PRIMARY KEY,
  price_per_case numeric NOT NULL
);

CREATE TABLE IF NOT EXISTS ops.synthetic_calendar_weeks (
  iso_year int NOT NULL,
  iso_week int NOT NULL,
  PRIMARY KEY (iso_year, iso_week)
);

CREATE TABLE IF NOT EXISTS ops.synthetic_capacity_weekly (
  agent_id text NOT NULL,
  team_id  text NOT NULL,
  iso_year int NOT NULL,
  iso_week int NOT NULL,
  capacity_hours numeric NOT NULL,
  PRIMARY KEY (agent_id, iso_year, iso_week)
);

CREATE TABLE IF NOT EXISTS ops.synthetic_budget_weekly (
  team_id       text NOT NULL,
  iso_year      int NOT NULL,
  iso_week      int NOT NULL,
  planned_hours numeric NOT NULL,
  planned_cost  numeric NOT NULL,
  PRIMARY KEY (team_id, iso_year, iso_week)
);

CREATE TABLE IF NOT EXISTS ops.synthetic_weekly_perf (
  agent_id         text NOT NULL,
  team_id          text NOT NULL,
  iso_year         int NOT NULL,
  iso_week         int NOT NULL,
  hours            numeric NOT NULL,
  cases_total      numeric NOT NULL,
  cases_standard   int NOT NULL,
  cases_priority   int NOT NULL,
  cases_escalation int NOT NULL,
  revenue          numeric NOT NULL,
  out_hours_flag   int NOT NULL,
  out_cases_flag   int NOT NULL,
  hours_mean       numeric,
  cases_mean       numeric,
  PRIMARY KEY (agent_id, iso_year, iso_week)
);