"""Validate and analyze the generated eye-care visit dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "eye_hospital_1000_synthetic_patient_records.csv"
OUT = ROOT / "outputs" / "eda"


def main():
    if not DATA.exists():
        raise FileNotFoundError(
            f"{DATA} not found. Run: python python/generate_dataset.py"
        )
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA, parse_dates=["visit_date"])

    required = [
        "visit_id", "patient_id", "visit_date", "department",
        "appointment_status", "waiting_time_min", "consultation_fee"
    ]
    missing_columns = sorted(set(required) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    checks = {
        "row_count": len(df) == 1000,
        "unique_visit_ids": df["visit_id"].is_unique,
        "no_missing_required": not df[required].isna().any().any(),
        "valid_age": df["age"].between(0, 100).all(),
        "nonnegative_wait": df["waiting_time_min"].ge(0).all(),
        "nonnegative_fee": df["consultation_fee"].ge(0).all(),
        "valid_status": df["appointment_status"].isin(
            ["Completed", "Cancelled", "No-show"]
        ).all(),
    }
    print("\nDATA QUALITY CHECKS")
    for name, passed in checks.items():
        print(f"{name:24} {'PASS' if passed else 'FAIL'}")
    if not all(checks.values()):
        raise ValueError("One or more data quality checks failed.")

    total = len(df)
    completed = (df["appointment_status"] == "Completed").sum()
    summary = pd.DataFrame([{
        "total_visits": total,
        "unique_patients": df["patient_id"].nunique(),
        "completed_visits": int(completed),
        "completion_rate_pct": round(completed / total * 100, 2),
        "avg_waiting_time_min": round(df["waiting_time_min"].mean(), 2),
        "total_synthetic_billed_fees_inr": round(df["consultation_fee"].sum(), 2),
        "avg_satisfaction": round(df["satisfaction_rating"].mean(), 2),
    }])
    summary.to_csv(OUT / "kpi_summary.csv", index=False)
    print("\nKPI SUMMARY")
    print(summary.to_string(index=False))

    sns.set_theme(style="whitegrid")
    charts = [
        ("visits_by_department.png",
         lambda: sns.countplot(data=df, y="department",
                               order=df["department"].value_counts().index)),
        ("appointment_status.png",
         lambda: sns.countplot(data=df, x="appointment_status",
                               order=["Completed", "Cancelled", "No-show"])),
        ("average_wait_by_department.png",
         lambda: sns.barplot(data=df, y="department", x="waiting_time_min",
                             errorbar=None, estimator="mean",
                             order=df.groupby("department")["waiting_time_min"]
                             .mean().sort_values(ascending=False).index)),
        ("billed_fees_by_department.png",
         lambda: sns.barplot(data=df, y="department", x="consultation_fee",
                             errorbar=None, estimator="sum",
                             order=df.groupby("department")["consultation_fee"]
                             .sum().sort_values(ascending=False).index)),
        ("visits_by_branch.png",
         lambda: sns.countplot(data=df, x="branch",
                               order=df["branch"].value_counts().index)),
    ]
    for filename, draw in charts:
        fig, ax = plt.subplots(figsize=(10, 6))
        draw()
        ax.set_title(filename.replace("_", " ").replace(".png", "").title())
        fig.tight_layout()
        fig.savefig(OUT / filename, dpi=160, bbox_inches="tight")
        plt.close(fig)

    print(f"\nEDA outputs saved to: {OUT}")


if __name__ == "__main__":
    main()
