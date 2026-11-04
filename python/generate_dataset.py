"""Generate a reproducible, fictional 1,000-row eye-care visit dataset."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N = 1000
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "eye_hospital_1000_synthetic_patient_records.csv"


def main():
    rng = np.random.default_rng(SEED)
    departments = np.array([
        "General Ophthalmology", "Cataract", "Retina",
        "Glaucoma", "Cornea", "Pediatric Ophthalmology",
        "Optometry", "Oculoplasty"
    ])
    dept_probs = np.array([.24, .17, .13, .11, .10, .08, .12, .05])
    branches = np.array(["Kurnool", "Hyderabad", "Bengaluru"])
    branch_probs = [.35, .40, .25]
    doctors = np.array([
        "Dr. A. Rao", "Dr. S. Reddy", "Dr. P. Kumar",
        "Dr. M. Sharma", "Dr. N. Iyer", "Dr. K. Das",
        "Dr. V. Menon", "Dr. R. Gupta"
    ])
    first_names = np.array([
        "Aarav", "Ananya", "Vihaan", "Diya", "Arjun", "Ishita",
        "Rohan", "Meera", "Kiran", "Saanvi", "Aditya", "Priya",
        "Rahul", "Nisha", "Sai", "Kavya"
    ])
    last_names = np.array([
        "Rao", "Reddy", "Kumar", "Sharma", "Patel", "Iyer",
        "Das", "Naidu", "Gupta", "Menon", "Verma", "Joshi"
    ])

    visit_dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(
        rng.integers(0, 365, N), unit="D"
    )
    department = rng.choice(departments, N, p=dept_probs)
    branch = rng.choice(branches, N, p=branch_probs)
    status = rng.choice(["Completed", "Cancelled", "No-show"], N,
                        p=[.78, .13, .09])
    age = np.clip(np.rint(rng.normal(42, 19, N)), 1, 95).astype(int)
    gender = rng.choice(["Female", "Male", "Other"], N, p=[.47, .51, .02])

    dept_wait = {
        "General Ophthalmology": 22, "Cataract": 28, "Retina": 35,
        "Glaucoma": 30, "Cornea": 26, "Pediatric Ophthalmology": 24,
        "Optometry": 16, "Oculoplasty": 32
    }
    wait = np.array([rng.normal(dept_wait[d], 10) for d in department])
    waiting_time = np.clip(np.rint(wait), 2, 120).astype(int)

    dept_fee = {
        "General Ophthalmology": 450, "Cataract": 900, "Retina": 1100,
        "Glaucoma": 750, "Cornea": 850, "Pediatric Ophthalmology": 600,
        "Optometry": 300, "Oculoplasty": 1000
    }
    fees = np.array([dept_fee[d] for d in department], dtype=float)
    fees = np.maximum(0, np.rint(fees * rng.normal(1, .15, N) / 10) * 10)

    satisfaction = np.clip(
        np.rint(4.4 - waiting_time / 45 + rng.normal(0, .65, N)), 1, 5
    ).astype(int)
    satisfaction = pd.array(satisfaction, dtype="Int64")
    satisfaction[np.array(status) != "Completed"] = pd.NA

    df = pd.DataFrame({
        "visit_id": [f"VIS{n:04d}" for n in range(1, N + 1)],
        "patient_id": [f"PAT{n:04d}" for n in rng.integers(1, 701, N)],
        "patient_name": [
            f"{rng.choice(first_names)} {rng.choice(last_names)}" for _ in range(N)
        ],
        "age": age,
        "gender": gender,
        "visit_date": pd.to_datetime(visit_dates).strftime("%Y-%m-%d"),
        "branch": branch,
        "department": department,
        "doctor": rng.choice(doctors, N),
        "waiting_time_min": waiting_time,
        "consultation_fee": fees,
        "appointment_status": status,
        "payment_method": rng.choice(
            ["Cash", "UPI", "Card", "Insurance"], N,
            p=[.18, .42, .25, .15]
        ),
        "satisfaction_rating": satisfaction
    })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Created: {OUT}")
    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    print("Synthetic data only. Fixed seed:", SEED)


if __name__ == "__main__":
    main()
