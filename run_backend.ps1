Set-Location "$PSScriptRoot\backend"
if (!(Test-Path ".venv")) { python -m venv .venv }
& ".\.venv\Scripts\Activate.ps1"
pip install -r requirements.txt
if (!(Test-Path "app\ml\models\crop_model.joblib")) { python -m app.ml.train }
pytest
uvicorn app.main:app --reload
