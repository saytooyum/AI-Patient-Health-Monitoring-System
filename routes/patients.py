from flask import (
    render_template,
    request,
    redirect,
    session,
    jsonify
)

from app import app
from database import get_db
@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Doctor":
        return "Access Denied"

    if request.method == "POST":

        patient_name = request.form["patient_name"]
        age = request.form["age"]
        gender = request.form["gender"]

        username = request.form["username"]
        password = request.form["password"]

        db, cursor = get_db()

        # Generate patient code

        cursor.execute("""
            SELECT COUNT(*)
            FROM patients
        """)

        patient_count = cursor.fetchone()[0] + 1

        patient_code = f"PAT{patient_count:03d}"

        # Insert patient

        cursor.execute("""
            INSERT INTO patients
            (
                patient_code,
                patient_name,
                age,
                gender
            )
            VALUES (%s,%s,%s,%s)
        """, (
            patient_code,
            patient_name,
            age,
            gender
        ))

        db.commit()

        patient_id = cursor.lastrowid

        # Create login

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                role,
                patient_id
            )
            VALUES (%s,%s,'Patient',%s)
        """, (
            username,
            password,
            patient_id
        ))

        db.commit()

        cursor.close()
        db.close()

        return redirect("/dashboard")

    return render_template("add_patient.html")
#=====================================
@app.route("/patients")
def patients():

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Doctor":
        return "Access Denied"

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            p.patient_id,
            p.patient_code,
            p.patient_name,
            p.age,
            p.gender,

            (
                SELECT risk_status
                FROM patient_data
                WHERE patient_id = p.patient_id
                ORDER BY created_at DESC
                LIMIT 1
            ) AS risk_status

        FROM patients p

        ORDER BY p.patient_name
    """)

    patients = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "patients.html",
        patients=patients
    )
#===========================================
#Patient ID route
#==========================================
@app.route("/patient/<int:patient_id>")
def patient_profile(patient_id):

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Doctor":
        return "Access Denied"

    db, cursor = get_db()

    # -----------------------------
    # Patient Information
    # -----------------------------
    cursor.execute("""
        SELECT
            patient_code,
            patient_name,
            age,
            gender
        FROM patients
        WHERE patient_id=%s
    """, (patient_id,))

    patient = cursor.fetchone()

    # -----------------------------
    # Latest Vital Signs
    # -----------------------------
    cursor.execute("""
        SELECT
            heart_rate,
            spo2,
            ecg_value,
            temperature,
            risk_status,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at DESC
        LIMIT 1
    """, (patient_id,))

    latest = cursor.fetchone()
    # -----------------------------
    # Average Vital Signs
    # -----------------------------
    cursor.execute("""
        SELECT
            ROUND(AVG(heart_rate), 1),
            ROUND(AVG(spo2), 1),
            ROUND(AVG(temperature), 1)
        FROM patient_data
        WHERE patient_id=%s
    """, (patient_id,))

    averages = cursor.fetchone()
    # -----------------------------
    # Last 5 Readings
    # -----------------------------
    cursor.execute("""
        SELECT
            heart_rate,
            spo2,
            temperature,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at DESC
        LIMIT 5
    """, (patient_id,))

    recent_readings = cursor.fetchall()
    # -----------------------------
    # Complete History
    # -----------------------------
    cursor.execute("""
        SELECT
            heart_rate,
            spo2,       
            ecg_value,
            temperature,
            risk_status,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at DESC
    """, (patient_id,))

    history = cursor.fetchall()

    # -----------------------------
    # Doctor Notes
    # -----------------------------
    cursor.execute("""
        SELECT
            doctor_name,
            note,
            created_at
        FROM doctor_notes
        WHERE patient_id=%s
        ORDER BY created_at DESC
    """, (patient_id,))

    notes = cursor.fetchall()
    # -----------------------------
    # Health Summary Engine
    # -----------------------------

    health_summary = []

    # Heart Rate
    if latest and latest[0] is not None:

        hr = latest[0]

        if hr < 60:
            health_summary.append({
                "parameter": "Heart Rate",
                "status": "Low",
                "message": f"Heart rate is below the normal range ({hr} BPM).",
                "color": "warning"
            })

        elif hr > 100:
            health_summary.append({
                "parameter": "Heart Rate",
                "status": "High",
                "message": f"Heart rate is elevated ({hr} BPM).",
                "color": "warning"
            })

        else:
            health_summary.append({
                "parameter": "Heart Rate",
                "status": "Normal",
                "message": f"Heart rate is normal ({hr} BPM).",
                "color": "success"
            })


    # SpO₂
    if latest and latest[1] is not None:

        spo2 = latest[1]

        if spo2 < 90:
            health_summary.append({
                "parameter": "SpO₂",
                "status": "Critical",
                "message": f"SpO₂ is critically low ({spo2}%).",
                "color": "danger"
            })

        elif spo2 < 95:
            health_summary.append({
                "parameter": "SpO₂",
                "status": "Low",
                "message": f"SpO₂ is slightly below normal ({spo2}%).",
                "color": "warning"
            })

        else:
            health_summary.append({
                "parameter": "SpO₂",
                "status": "Normal",
                "message": f"SpO₂ is within the normal range ({spo2}%).",
                "color": "success"
            })


    # Temperature
    if latest and latest[3] is not None:

        temp = latest[3]

        if temp > 39:
            health_summary.append({
                "parameter": "Temperature",
                "status": "High Fever",
                "message": f"Temperature indicates high fever ({temp}°C).",
                "color": "danger"
            })

        elif temp > 37.5:
            health_summary.append({
                "parameter": "Temperature",
                "status": "Mild Fever",
                "message": f"Temperature is slightly elevated ({temp}°C).",
                "color": "warning"
            })

        else:
            health_summary.append({
                "parameter": "Temperature",
                "status": "Normal",
                "message": f"Temperature is normal ({temp}°C).",
                "color": "success"
            })
    cursor.close()
    db.close()

    return render_template(
    "patient_profile.html",
    patient=patient,
    latest=latest,
    history=history,
    patient_id=patient_id,
    notes=notes,
    averages=averages,
    recent_readings=recent_readings,
    health_summary=health_summary
)
@app.route("/add-note/<int:patient_id>", methods=["POST"])
def add_note(patient_id):

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Doctor":
        return "Access Denied"

    note = request.form["note"]
    doctor = session["username"]

    db, cursor = get_db()

    cursor.execute("""
        INSERT INTO doctor_notes
        (
            patient_id,
            doctor_name,
            note
        )
        VALUES (%s, %s, %s)
    """, (
        patient_id,
        doctor,
        note
    ))

    db.commit()

    cursor.close()
    db.close()

    return redirect(f"/patient/{patient_id}")
@app.route("/patient-dashboard")
def patient_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Patient":
        return "Access Denied"

    patient_id = session["patient_id"]

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            patient_code,
            patient_name,
            age,
            gender
        FROM patients
        WHERE patient_id=%s
    """, (patient_id,))

    patient = cursor.fetchone()

    cursor.execute("""
        SELECT
            heart_rate,
            spo2,       
            ecg_value,
            temperature,
            risk_status,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at DESC
        LIMIT 1
    """, (patient_id,))

    latest_data = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "patient_dashboard.html",
        patient=patient,
        latest_data=latest_data
    )
@app.route("/start-monitoring/<int:patient_id>", methods=["POST"])
def start_monitoring(patient_id):

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "Doctor":
        return "Access Denied"

    db, cursor = get_db()

    # Remove previous active patient
    cursor.execute("DELETE FROM active_monitoring")

    # Set new active patient
    cursor.execute("""
        INSERT INTO active_monitoring
        (patient_id, started_by)
        VALUES (%s, %s)
    """, (
        patient_id,
        session["username"]
    ))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/patients")