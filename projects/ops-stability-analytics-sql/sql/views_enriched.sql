-- Schema defensivo
CREATE SCHEMA IF NOT EXISTS ops;

-- Vista ejecutiva de finanzas/operaciones (no duplica columnas del USING)
CREATE OR REPLACE VIEW ops.v_exec_finance AS
WITH cap_team AS (
  SELECT team_id, iso_year, iso_week, SUM(capacity_hours) AS capacity_hours
  FROM ops.synthetic_capacity_weekly
  GROUP BY team_id, iso_year, iso_week
), wp AS (
  SELECT
    w.team_id, w.iso_year, w.iso_week,
    SUM(w.revenue) AS revenue,
    SUM(w.hours)   AS hours,
    SUM(w.cases_total) AS cases,
    SUM(w.hours_mean)  AS hours_mean,
    SUM(w.cases_mean)  AS cases_mean
  FROM ops.synthetic_weekly_perf w
  GROUP BY w.team_id, w.iso_year, w.iso_week
), team_hourly AS (
  SELECT team_id, AVG(hourly_cost) AS hourly_cost
  FROM ops.synthetic_agent
  GROUP BY team_id
)
SELECT
  w.team_id,
  w.iso_year,
  w.iso_week,
  w.revenue,
  w.hours,
  w.cases,
  (w.hours * th.hourly_cost) AS cost_real,
  (w.revenue - (w.hours * th.hourly_cost)) AS margin,
  (w.hours / NULLIF(ct.capacity_hours,0)) AS utilization,
  ((w.hours - b.planned_hours) / NULLIF(b.planned_hours,0)) AS hours_variance_pct,
  (((w.hours * th.hourly_cost) - b.planned_cost) / NULLIF(b.planned_cost,0)) AS cost_variance_pct
FROM wp w
LEFT JOIN cap_team ct
  ON ct.team_id = w.team_id AND ct.iso_year = w.iso_year AND ct.iso_week = w.iso_week
LEFT JOIN ops.synthetic_budget_weekly b
  ON b.team_id = w.team_id AND b.iso_year = w.iso_year AND b.iso_week = w.iso_week
LEFT JOIN team_hourly th
  ON th.team_id = w.team_id;