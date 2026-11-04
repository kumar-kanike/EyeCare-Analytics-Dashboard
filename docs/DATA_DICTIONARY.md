# Data Dictionary

The generated dataset contains one row per patient visit.

| Column | Type | Description |
|---|---|---|
| visit_id | Text | Unique visit identifier |
| patient_id | Text | Synthetic patient identifier; may repeat across visits |
| patient_name | Text | Fictional patient display name |
| age | Integer | Patient age in years |
| gender | Category | Female, Male or Other |
| visit_date | Date | Visit date |
| branch | Category | Synthetic hospital branch |
| department | Category | Eye-care department visited |
| doctor | Text | Fictional doctor name |
| waiting_time_min | Integer | Waiting time in minutes |
| consultation_fee | Decimal | Synthetic billed fee in INR |
| appointment_status | Category | Completed, Cancelled or No-show |
| payment_method | Category | Cash, UPI, Card or Insurance |
| satisfaction_rating | Integer / blank | Synthetic rating from 1 to 5; may be blank for incomplete visits |

## Data quality rules

- `visit_id` must be unique and non-null.
- `patient_id`, `visit_date`, `department` and `appointment_status` must be populated.
- Age must be between 0 and 100.
- Waiting time and fee must be non-negative.
- Satisfaction rating must be blank or an integer from 1 to 5.
- Categories must use consistent spelling and capitalization.
