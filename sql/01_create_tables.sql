-- EyeCare Analytics Dashboard | SQLite-compatible schema
DROP TABLE IF EXISTS patient_visits;

CREATE TABLE patient_visits (
    visit_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    patient_name TEXT,
    age INTEGER CHECK (age BETWEEN 0 AND 100),
    gender TEXT CHECK (gender IN ('Female', 'Male', 'Other')),
    visit_date TEXT NOT NULL,
    branch TEXT,
    department TEXT NOT NULL,
    doctor TEXT,
    waiting_time_min INTEGER CHECK (waiting_time_min >= 0),
    consultation_fee REAL CHECK (consultation_fee >= 0),
    appointment_status TEXT NOT NULL
        CHECK (appointment_status IN ('Completed', 'Cancelled', 'No-show')),
    payment_method TEXT,
    satisfaction_rating INTEGER
        CHECK (satisfaction_rating IS NULL OR satisfaction_rating BETWEEN 1 AND 5)
);

CREATE INDEX idx_visits_date ON patient_visits(visit_date);
CREATE INDEX idx_visits_department ON patient_visits(department);
CREATE INDEX idx_visits_branch ON patient_visits(branch);
CREATE INDEX idx_visits_status ON patient_visits(appointment_status);
