-- 1. Overall KPIs
SELECT
    COUNT(*) AS total_visits,
    SUM(CASE WHEN appointment_status = 'Completed' THEN 1 ELSE 0 END) AS completed_visits,
    ROUND(100.0 * SUM(CASE WHEN appointment_status = 'Completed' THEN 1 ELSE 0 END)
          / NULLIF(COUNT(*), 0), 2) AS completion_rate_pct,
    ROUND(AVG(waiting_time_min), 2) AS avg_waiting_time_min,
    ROUND(SUM(consultation_fee), 2) AS total_synthetic_billed_fees
FROM patient_visits;

-- 2. Department demand and operational performance
SELECT
    department,
    COUNT(*) AS total_visits,
    ROUND(AVG(waiting_time_min), 2) AS avg_waiting_time_min,
    ROUND(SUM(consultation_fee), 2) AS synthetic_billed_fees
FROM patient_visits
GROUP BY department
ORDER BY total_visits DESC;

-- 3. Appointment outcomes
SELECT
    appointment_status,
    COUNT(*) AS visits,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM patient_visits), 2) AS share_pct
FROM patient_visits
GROUP BY appointment_status
ORDER BY visits DESC;

-- 4. Branch performance
SELECT
    branch,
    COUNT(*) AS total_visits,
    COUNT(DISTINCT patient_id) AS unique_patients,
    ROUND(AVG(waiting_time_min), 2) AS avg_waiting_time_min,
    ROUND(SUM(consultation_fee), 2) AS synthetic_billed_fees
FROM patient_visits
GROUP BY branch
ORDER BY total_visits DESC;

-- 5. Monthly visit trend
SELECT
    substr(visit_date, 1, 7) AS visit_month,
    COUNT(*) AS total_visits,
    SUM(CASE WHEN appointment_status = 'Completed' THEN 1 ELSE 0 END) AS completed_visits
FROM patient_visits
GROUP BY substr(visit_date, 1, 7)
ORDER BY visit_month;

-- 6. Payment method mix
SELECT
    payment_method,
    COUNT(*) AS transactions,
    ROUND(SUM(consultation_fee), 2) AS synthetic_billed_fees
FROM patient_visits
GROUP BY payment_method
ORDER BY transactions DESC;

-- 7. Satisfaction by waiting-time band
SELECT
    CASE
        WHEN waiting_time_min < 15 THEN 'Under 15 min'
        WHEN waiting_time_min < 30 THEN '15-29 min'
        WHEN waiting_time_min < 60 THEN '30-59 min'
        ELSE '60+ min'
    END AS waiting_time_band,
    COUNT(satisfaction_rating) AS rated_visits,
    ROUND(AVG(satisfaction_rating), 2) AS avg_satisfaction
FROM patient_visits
GROUP BY waiting_time_band
ORDER BY MIN(waiting_time_min);

-- 8. Data quality checks
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT visit_id) AS unique_visit_ids,
    SUM(CASE WHEN visit_id IS NULL OR patient_id IS NULL OR visit_date IS NULL
                  OR department IS NULL OR appointment_status IS NULL
             THEN 1 ELSE 0 END) AS rows_with_required_nulls,
    SUM(CASE WHEN age NOT BETWEEN 0 AND 100 THEN 1 ELSE 0 END) AS invalid_ages,
    SUM(CASE WHEN waiting_time_min < 0 OR consultation_fee < 0 THEN 1 ELSE 0 END)
        AS invalid_nonnegative_values
FROM patient_visits;
