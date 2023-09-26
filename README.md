# Retrieval Augmented Generation (RAG) Service with FastAPI

This is a RAG Service in FastAPI.

## Notes

- For VS Code to pick up poetry environment:
  - poetry config virtualenvs.in-project true
- Poetry:
  - poetry install --with dev
  - poetry run ./run.sh
- Docker:
  - docker build --progress=plain --no-cache -t rag-fastapi .
  - docker run -p 5000:5000 rag-fastapi
- Precommit:
  - pre-commit install
  - pre-commit run --all-files
