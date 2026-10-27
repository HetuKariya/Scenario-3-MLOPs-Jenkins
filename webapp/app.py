import pickle
import numpy
import os
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

DB_BASE_URL = "http://dbapp:8001"

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "gaussian_nb_model.pkl")
with open(file=MODEL_PATH, mode="rb") as f:
    model = pickle.load(f)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def make_pred():
    if request.method == "GET":
        return redirect(url_for("index"))

    try:
        sl = float(request.form["sepal_length"])
        sw = float(request.form["sepal_width"])
        pl = float(request.form["petal_length"])
        pw = float(request.form["petal_width"])
    except (KeyError, ValueError):
        return render_template(
            "result.html",
            prediction="Invalid input. Please enter valid numbers for all fields.",
            inputs=None,
        )

    inp = numpy.array([[sl, sw, pl, pw]])
    pred = str(model.predict(inp)[0])

    try:
        resp = requests.post(
            f"{DB_BASE_URL}/add_record",
            json={"sl": sl, "sw": sw, "pl": pl, "pw": pw, "prediction": pred},
            timeout=5,
        )
        resp.raise_for_status()
    except requests.RequestException:
        # prediction still works even if saving fails
        pred_msg = f"{pred} (warning: could not save to database)"
    else:
        pred_msg = pred

    return render_template(
        "result.html",
        prediction=pred_msg,
        inputs={"sl": sl, "sw": sw, "pl": pl, "pw": pw},
    )


@app.route("/show", methods=["GET", "POST"])
def show_records():
    try:
        resp = requests.get(f"{DB_BASE_URL}/records", timeout=5)
        resp.raise_for_status()
        records = resp.json()
    except requests.RequestException:
        records = []
    return render_template("records.html", records=records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)