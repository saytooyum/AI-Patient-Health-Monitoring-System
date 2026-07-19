from flask import(
    jsonify,
    request
)
from utils import calculate_risk
from app import app
from database import get_db
@app.route("/patient-data", methods=["POST"])
def patient_data():

    try:

        db, cursor = get_db()

        data = request.json

        # -----------------------------
        # Sensor Data
        # -----------------------------

        heart_rate = data["heart_rate"]
        spo2 = data["spo2"]
        temperature = data["temperature"]
        ecg_value = data["ecg_value"]

        # -----------------------------
        # Get Active Patient
        # -----------------------------

        cursor.execute("""
            SELECT patient_id
            FROM active_monitoring
            LIMIT 1
        """)

        active = cursor.fetchone()

        if active is None:

            cursor.close()
            db.close()

            return jsonify({
                "error": "No patient is currently being monitored."
            }), 400

        patient_id = active[0]

        # -----------------------------
        # Calculate Risk
        # -----------------------------

        risk_status = calculate_risk(
            heart_rate,
            temperature,
            spo2
        )

        # -----------------------------
        # Store Data
        # -----------------------------

        sql = """
        INSERT INTO patient_data
        (
            patient_id,
            heart_rate,
            spo2,
            ecg_value,
            temperature,
            risk_status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            patient_id,
            heart_rate,
            spo2,
            ecg_value,
            temperature,
            risk_status
        )

        cursor.execute(sql, values)

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "message": "Patient data stored successfully",
            "risk_status": risk_status
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
# =====================================
# GET ALL SENSOR DATA
# =====================================

@app.route("/patient-data", methods=["GET"])
def get_patient_data():

    db, cursor = get_db()

    cursor.execute("""
        SELECT *
        FROM patient_data
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({
            "id": row[0],
            "patient_id": row[1],
            "heart_rate": row[2],
            "ecg_value": row[3],
            "temperature": row[4],
            "risk_status": row[5],
            "created_at": str(row[6])
        })
    cursor.close()
    db.close()
    
    return jsonify(result)

@app.route("/patient-heart-rate/<int:patient_id>")
def patient_heart_rate(patient_id):

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            heart_rate,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at ASC
    """, (patient_id,))

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
#====================================
#patient temperature api
#=====================================
@app.route("/patient-temperature/<int:patient_id>")
def patient_temperature(patient_id):

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            temperature,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at ASC
    """, (patient_id,))

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
#======================================
#Patient ECG API
#======================================
@app.route("/patient-ecg/<int:patient_id>")
def patient_ecg(patient_id):

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            ecg_value,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at ASC
    """, (patient_id,))

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
@app.route("/patient-spo2/<int:patient_id>")
def patient_spo2(patient_id):

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            spo2,
            created_at
        FROM patient_data
        WHERE patient_id=%s
        ORDER BY created_at ASC
    """, (patient_id,))

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