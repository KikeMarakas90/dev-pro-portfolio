INSERT INTO ops.team(team_id, team_name) VALUES
('T1','Team 1'),('T2','Team 2'),('T3','Team 3'),('T4','Team 4'),('T5','Team 5'),('T6','Team 6')
ON CONFLICT DO NOTHING;

-- 60 agentes a T1..T6
WITH a AS (SELECT generate_series(1,60) i)
INSERT INTO ops.agent(agent_id, team_id, hire_date)
SELECT
  'AG' || lpad(i::text,3,'0'),
  'T' || ((i % 6)+1),
  (CURRENT_DATE - (50 + i) * interval '1 day')::date
FROM a
ON CONFLICT DO NOTHING;

-- Calendario (últimas 16 semanas)
INSERT INTO ops.calendar(dt, iso_week, iso_year)
SELECT d::date,
       EXTRACT(WEEK FROM d)::int,
       EXTRACT(YEAR FROM d)::int
FROM generate_series(CURRENT_DATE - interval '112 day', CURRENT_DATE, interval '1 day') d
ON CONFLICT DO NOTHING;

-- Hechos semanales sintéticos
WITH weeks AS (
  SELECT DISTINCT iso_week::int, iso_year::int FROM ops.calendar
),
base AS (
  SELECT ag.agent_id, ag.team_id, w.iso_week, w.iso_year
  FROM ops.agent ag CROSS JOIN weeks w
),
rnd AS (
  SELECT agent_id, team_id, iso_week, iso_year,
         5.5 + random()*1.5   AS hours_mean,
         17  + random()*6     AS cases_mean
  FROM base
)
INSERT INTO ops.weekly_perf(agent_id, team_id, iso_week, iso_year, hours_mean, cases_mean, out_hours_flag, out_cases_flag)
SELECT agent_id, team_id, iso_week, iso_year,
       hours_mean, cases_mean,
       CASE WHEN hours_mean < 5.0 OR hours_mean > 7.5 THEN 1 ELSE 0 END,
       CASE WHEN cases_mean < 12  OR cases_mean > 25  THEN 1 ELSE 0 END
FROM rnd
ON CONFLICT DO NOTHING;

-- Stability por agente (CV y CVM sin anidar agregados)
WITH med AS (
  SELECT
    wp.agent_id,
    MIN(wp.team_id) AS team_id,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY wp.hours_mean) AS med_hours,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY wp.cases_mean) AS med_cases
  FROM ops.weekly_perf wp
  GROUP BY wp.agent_id
),
dev AS (
  SELECT
    wp.agent_id,
    ABS(wp.hours_mean - m.med_hours)  AS dev_hours,
    ABS(wp.cases_mean - m.med_cases)  AS dev_cases
  FROM ops.weekly_perf wp
  JOIN med m USING (agent_id)
),
mad AS (
  SELECT
    agent_id,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY dev_hours) AS mad_hours,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY dev_cases) AS mad_cases
  FROM dev
  GROUP BY agent_id
),
agg AS (
  SELECT
    m.agent_id,
    m.team_id,
    STDDEV_SAMP(wp.hours_mean) / NULLIF(AVG(wp.hours_mean), 0)  AS cv_hours,
    STDDEV_SAMP(wp.cases_mean) / NULLIF(AVG(wp.cases_mean), 0)  AS cv_cases,
    m.med_hours,
    m.med_cases,
    md.mad_hours,
    md.mad_cases
  FROM ops.weekly_perf wp
  JOIN med m  USING (agent_id)
  JOIN mad md USING (agent_id)
  GROUP BY m.agent_id, m.team_id, m.med_hours, m.med_cases, md.mad_hours, md.mad_cases
),
ranked AS (
  SELECT
    agent_id,
    team_id,
    cv_hours,
    (1.4826 * mad_hours / NULLIF(med_hours, 0)) AS cvm_hours,
    cv_cases,
    (1.4826 * mad_cases / NULLIF(med_cases, 0)) AS cvm_cases,
    NTILE(4) OVER (ORDER BY cv_hours) AS quartile_efficiency
  FROM agg
)
INSERT INTO ops.agent_stability(agent_id, team_id, cv_hours, cvm_hours, cv_cases, cvm_cases, quartile_efficiency)
SELECT agent_id, team_id, cv_hours, cvm_hours, cv_cases, cvm_cases, quartile_efficiency
FROM ranked
ON CONFLICT (agent_id) DO UPDATE
SET team_id = EXCLUDED.team_id,
    cv_hours = EXCLUDED.cv_hours,
    cvm_hours = EXCLUDED.cvm_hours,
    cv_cases = EXCLUDED.cv_cases,
    cvm_cases = EXCLUDED.cvm_cases,
    quartile_efficiency = EXCLUDED.quartile_efficiency;