from flask import jsonify
from app import app
from database import get_db
@app.route("/patient-report")
def patient_report():

    db, cursor = get_db()

    cursor.execute("""
        SELECT
            p.patient_code,
            p.patient_name,
            p.age,
            p.gender,
            d.heart_rate,
            d.ecg_value,
            d.temperature,
            d.risk_status,
            d.created_at

        FROM patients p

        JOIN patient_data d
        ON p.patient_id = d.patient_id

        ORDER BY d.created_at DESC
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({
            "patient_code": row[0],
            "patient_name": row[1],
            "age": row[2],
            "gender": row[3],
            "heart_rate": row[4],
            "ecg_value": row[5],
            "temperature": row[6],
            "risk_status": row[7],
            "created_at": str(row[8])
        })
    cursor.close()
    db.close()
    return jsonify(result)