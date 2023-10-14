# Retrieval Augmented Generation (RAG) Service with FastAPI

This is a RAG Service in FastAPI.

## Notes

- For VS Code to pick up poetry environment:
  - poetry config virtualenvs.in-project true
- Poetry:
  - poetry install --with dev
  - poetry run ./run.sh
- Docker:
  - docker build --progress=plain --no-cache --platform linux/amd64 -t ghcr.io/acn-catwalk-llmops/rag-fastapi:0.0.1 .
  - docker run -p 8000:8000 rag-fastapi
  - login to GitHub container registry
    - export CR_TOKEN={YOUR_GH_TOKEN}
    - echo $CR_TOKEN | docker login ghcr.io -u {YOUR_GH_USERNAME_NOT_EMAIL} --password-stdin
  - docker push ghcr.io/acn-catwalk-llmops/rag-fastapi:0.0.1
- Precommit:
  - pre-commit install
  - pre-commit run --all-files
- Helm
  - helm install rag-service helm/rag-service
  - helm uninstall rag-service
  - helm template helm/rag-service

## TODOs

- test document loader
- evtl andere vector datenbank integrieren und probieren zu abstrahieren
