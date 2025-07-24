python -m venv venv
# Activation sous Windows
venv\Scripts\activate


uvicorn main:app --reload --port 8001
