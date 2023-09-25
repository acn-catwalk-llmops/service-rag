# Retrieval Augmented Generation (RAG) Service with FastAPI

This is a RAG Service wrapped FastAPI.

## Notes

- poetry install --with dev
- for vscode to pick up poetry environment: poetry config virtualenvs.in-project true
- poetry run ./run.sh
- Docker:
  - docker build --progress=plain --no-cache -t rag-fastapi .
  - docker run -p 5000:5000 rag-fastapi
- Precommit:
  - pre-commit install
  - pre-commit run --all-files
