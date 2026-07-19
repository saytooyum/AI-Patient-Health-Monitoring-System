from flask import (
    render_template,
    redirect,
    session,
    jsonify
)

from app import app
from database import get_db


# =====================================
# DOCTOR DASHBOARD
# =====================================

@app.route("/dashboard")
def dashboard():

    # -----------------------------
    # Authentication
    # -----------------------------

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Doctor":
        return "Access Denied"

    db, cursor = get_db()
# =====================================
# LATEST PATIENT RECORDS
# =====================================

    cursor.execute("""

    SELECT

        p.patient_code,
        p.patient_name,
        p.age,
        p.gender,

        d.heart_rate,
        d.spo2,
        d.ecg_value,
        d.temperature,
        d.risk_status,
        d.created_at

    FROM patients p

    JOIN patient_data d
    ON p.patient_id = d.patient_id

    WHERE d.created_at = (

        SELECT MAX(created_at)

        FROM patient_data

        WHERE patient_id = p.patient_id

    )

    ORDER BY d.created_at DESC

    """)

    rows = cursor.fetchall()    
# =====================================
# DASHBOARD STATISTICS
# =====================================

# Total Patients
    cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    """)

    total_patients = cursor.fetchone()[0]


    # Total Readings
    cursor.execute("""
    SELECT COUNT(*)
    FROM patient_data
    """)

    total_readings = cursor.fetchone()[0]


    # Average Heart Rate
    cursor.execute("""
    SELECT ROUND(AVG(heart_rate),2)
    FROM patient_data
    """)

    avg_hr = cursor.fetchone()[0]


# Average SpO₂
    cursor.execute("""
    SELECT ROUND(AVG(spo2),2)
    FROM patient_data
    """)

    avg_spo2 = cursor.fetchone()[0]


# Latest Critical Cases
    cursor.execute("""

    SELECT COUNT(*)

    FROM (

        SELECT
            patient_id,
            risk_status

        FROM patient_data pd

        WHERE created_at=(

            SELECT MAX(created_at)

            FROM patient_data

            WHERE patient_id=pd.patient_id

        )

    ) latest

    WHERE risk_status='Critical'

    """)

    critical_cases = cursor.fetchone()[0]  
    # =====================================
    # CURRENTLY MONITORED PATIENT
    # =====================================

    cursor.execute("""

    SELECT

        p.patient_code,
        p.patient_name,
        p.age,
        p.gender,

        d.heart_rate,
        d.spo2,
        d.temperature,
        d.ecg_value,
        d.risk_status,

        a.started_at

    FROM active_monitoring a

    JOIN patients p
    ON a.patient_id = p.patient_id

    JOIN patient_data d
    ON p.patient_id = d.patient_id

    WHERE d.created_at=(

        SELECT MAX(created_at)

        FROM patient_data

        WHERE patient_id=p.patient_id

    )

    LIMIT 1

    """)

    live_patient = cursor.fetchone()


# =====================================
# PATIENT PRIORITY QUEUE
# =====================================

    cursor.execute("""

    SELECT

        p.patient_id,
        p.patient_code,
        p.patient_name,

        d.heart_rate,
        d.spo2,
        d.temperature,
        d.risk_status

    FROM patients p

    JOIN patient_data d
    ON p.patient_id=d.patient_id

    WHERE d.created_at=(

        SELECT MAX(created_at)

        FROM patient_data

        WHERE patient_id=p.patient_id

    )

    ORDER BY

    CASE

    WHEN d.risk_status='Critical' THEN 1

    WHEN d.risk_status='Warning' THEN 2

    ELSE 3

    END,

    d.created_at DESC

    """)

    priority_patients = cursor.fetchall()


# =====================================
# CRITICAL ALERTS
# =====================================

    cursor.execute("""

    SELECT

        p.patient_code,
        p.patient_name,

        d.heart_rate,
        d.spo2,
        d.temperature

    FROM patients p

    JOIN patient_data d
    ON p.patient_id=d.patient_id

    WHERE d.created_at=(

        SELECT MAX(created_at)

        FROM patient_data

        WHERE patient_id=p.patient_id

    )

    AND d.risk_status='Critical'

    ORDER BY d.created_at DESC

    """)

    critical_alerts = cursor.fetchall()


# =====================================
# HOSPITAL STATUS
# =====================================

    normal_count = 0
    warning_count = 0
    critical_count = 0

    for patient in priority_patients:

        if patient[6] == "Normal":
         normal_count += 1

        elif patient[6] == "Warning":
            warning_count += 1

        else:
            critical_count += 1


    cursor.close()
    db.close()   
    return render_template(

        "dashboard.html",

        patient_records=rows,

        total_patients=total_patients,
        total_readings=total_readings,

        critical_cases=critical_cases,

        avg_hr=avg_hr,
        avg_spo2=avg_spo2,

        live_patient=live_patient,

        priority_patients=priority_patients,

        critical_alerts=critical_alerts,

        normal_count=normal_count,
        warning_count=warning_count,
        critical_count=critical_count

    )
# =====================================
# HEART RATE GRAPH
# =====================================

@app.route("/heart-rate-data")
def heart_rate_data():

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            heart_rate,
            created_at
        FROM patient_data
        ORDER BY created_at ASC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    labels = []
    values = []

    for row in rows:

        values.append(row[0])
        labels.append(str(row[1]))

    cursor.close()
    db.close()

    return jsonify({
        "labels": labels,
        "values": values
    })


# =====================================
# TEMPERATURE GRAPH
# =====================================

@app.route("/temperature-data")
def temperature_data():

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            temperature,
            created_at
        FROM patient_data
        ORDER BY created_at ASC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    labels = []
    values = []

    for row in rows:

        values.append(row[0])
        labels.append(str(row[1]))

    cursor.close()
    db.close()

    return jsonify({
        "labels": labels,
        "values": values
    })       