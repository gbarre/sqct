# SQCT

## Dev helper

### Run API for dev

```sh
python3 -m virtualenv venv
. venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt -r test-requirements.txt
FLASK_APP=server:app python -m flask db upgrade
gunicorn server:app --error-logfile - --bind=0.0.0.0:5000 --workers=1
```

### Access to API UI

<http://localhost:5000/v1/ui>
