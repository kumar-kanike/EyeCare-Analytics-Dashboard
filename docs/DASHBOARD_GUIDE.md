# Dashboard Build Guide

Use the generated CSV as the single source of truth. Confirm that date, numeric and category fields have the correct types before creating PivotTables or visuals.

## Six LibreOffice Calc PivotTables

Create each PivotTable on its own sheet. Use the following field layout:

| Sheet name | Rows | Columns | Values |
|---|---|---|---|
| Department_Analysis | department | — | Count of visit_id; Average of waiting_time_min |
| Appointment_Analysis | appointment_status | — | Count of visit_id |
| Waiting_Time_Analysis | department | appointment_status | Average of waiting_time_min |
| Revenue_Analysis | department | payment_method | Sum of consultation_fee |
| Branch_Analysis | branch | department | Count of visit_id; Sum of consultation_fee |
| Satisfaction_Analysis | department | — | Average of satisfaction_rating; Count of visit_id |

Use filters/slicers where available for branch, visit_date, department and appointment_status. Format fees as INR and waiting time in minutes. Do not add the counts of visits and unique patients together; they are different metrics.

## Calc dashboard layout

**Top KPI row**
- Total Visits: count of visit_id
- Completed Visits: count where appointment_status = Completed
- Completion Rate: Completed Visits / Total Visits
- Average Waiting Time: average waiting_time_min
- Total Billed Fees: sum of consultation_fee (label clearly as synthetic billed fees)

**Charts**
1. Visits by Department — horizontal bar chart.
2. Appointment Status — doughnut or column chart.
3. Average Waiting Time by Department — bar chart.
4. Billed Fees by Department — column chart.
5. Visits by Branch — bar chart.
6. Average Satisfaction by Department — bar chart.

Add a clear title, reporting period, data note and consistent number formats. Avoid 3D charts.

## Power BI measures (DAX)

Assuming the imported table is named `patient_visits`:

```DAX
Total Visits =
COUNTROWS(patient_visits)

Completed Visits =
CALCULATE(
    [Total Visits],
    patient_visits[appointment_status] = "Completed"
)

Cancelled Visits =
CALCULATE(
    [Total Visits],
    patient_visits[appointment_status] = "Cancelled"
)

No-Show Visits =
CALCULATE(
    [Total Visits],
    patient_visits[appointment_status] = "No-show"
)

Completion Rate =
DIVIDE([Completed Visits], [Total Visits], 0)

Average Waiting Time =
AVERAGE(patient_visits[waiting_time_min])

Total Billed Fees =
SUM(patient_visits[consultation_fee])

Average Satisfaction =
AVERAGE(patient_visits[satisfaction_rating])

Unique Patients =
DISTINCTCOUNT(patient_visits[patient_id])
```

## Power BI page design

**Page 1 — Executive Overview**
- KPI cards: Total Visits, Completed Visits, Completion Rate, Average Waiting Time, Total Billed Fees.
- Bar chart: Visits by Department.
- Donut chart: Appointment Status.
- Line chart: Visits by Month.
- Slicers: Visit Date, Branch, Department.

**Page 2 — Operations**
- Average Waiting Time by Department.
- Waiting Time by Appointment Status.
- Visit Volume by Branch.
- Matrix: Branch × Department with visit count and average wait.

**Page 3 — Financial & Experience**
- Total Billed Fees by Department and Branch.
- Billed Fees by Payment Method.
- Average Satisfaction by Department.
- Satisfaction by Waiting-Time band (optional).

## Interpretation checklist

Write findings only after reading the actual pivot/Power BI results. Include at least three evidence-backed observations and two operational recommendations. Do not invent percentages or claim that waiting time causes low satisfaction. State that the data is synthetic in every exported report.
