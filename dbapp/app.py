import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.environ.get("DB_DIR", BASE_DIR)
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "predictions.db").replace("\\", "/")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sl = db.Column(db.Float)
    sw = db.Column(db.Float)
    pl = db.Column(db.Float)
    pw = db.Column(db.Float)
    prediction = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route("/add_record", methods=["POST"])
def add_record():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    try:
        record = Prediction(
            sl=data["sl"],
            sw=data["sw"],
            pl=data["pl"],
            pw=data["pw"],
            prediction=data["prediction"],
        )
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e.args[0]}"}), 400
    
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Record added successfully"}), 201

@app.route("/records", methods=["GET"])
def get_records():
    records = Prediction.query.all()
    return jsonify([
        {"id": r.id, "sl": r.sl, "sw": r.sw, "pl": r.pl, "pw": r.pw,
         "prediction": r.prediction}
        for r in records
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)