
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    session,
    url_for
)
from database import get_db
from config import *

app = Flask(__name__)
app.secret_key = SECRET_KEY
# =====================================
# HOME ROUTE
# =====================================

@app.route("/")
def home():
    return "Patient Health Monitoring System Running"
# =====================================
# RUN APP
# =====================================
from routes.auth import *
from routes.dashboard import *
from routes.patients import *
from routes.sensors import *
from routes.reports import *
from utils import calculate_risk
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
