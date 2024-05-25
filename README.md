# aiping-l2
#install poetry
poetry install
poetry shell
export OPENAI_API_KEY=API_KEY
uvicorn app.main:app --reload --port 3000 --host 0.0.0.0