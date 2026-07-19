from flask import (
    request,
    render_template,
    redirect,
    session
)

from app import app
from database import get_db


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db, cursor = get_db()

        cursor.execute("""
            SELECT
                user_id,
                username,
                role,
                patient_id
            FROM users
            WHERE username=%s
            AND password=%s
        """, (username, password))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:

            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[2]
            session["patient_id"] = user[3]

            if user[2] == "Doctor":
                return redirect("/dashboard")

            return redirect("/patient-dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")