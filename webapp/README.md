# Scenario 1 - Plain app.py (no Waitress)

Flask's built-in development server only. No production WSGI server, no nginx.

## Run

```powershell
cd scenario-1
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Notes

- Uses `app.run()` directly - single-threaded dev server, not meant for production
  load, but fine for local testing.
- `train_model.py` is included if you want to retrain `models/gaussian_nb_model.pkl`
  from `data/Iris (1).csv`.
