# Retrieval Augmented Generation (RAG) Service with FastAPI

This is a RAG Service in FastAPI.

## Setup GitHub Environment for CI/CD

The CI/CD depends on GitHub Environments and Environment Secrets. To set it up, we need to do the following things:

- Create `.env` from `.env.dist`
- Create GitHub access token with rights to modify deployments and run `export GITHUB_TOKEN={YOUR_GITHUB_TOKEN}`
- Run the script `.github/create_github_env.py`.

## Notes

- For VS Code to pick up poetry environment:
  - poetry config virtualenvs.in-project true
- Poetry:
  - poetry install --with dev
  - poetry run ./run.sh
- Docker:
  - build:
    - docker build --progress=plain --no-cache --platform linux/amd64 -t ghcr.io/acn-catwalk-llmops/rag-fastapi:0.0.1 .
    - docker build --platform linux/amd64 -t ghcr.io/acn-catwalk-llmops/rag-fastapi:0.0.1 .
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
- Git tag and push tag
  - git tag v1.2.3
  - git push origin v1.2.3

## TODOs

- test document loader
- evtl andere vector datenbank integrieren und probieren zu abstrahieren

## CI

### Github Actions Setup

- add AWS secrets AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to repository secret ("Settings" -> "Secrets and Variables" on repository page)
-

"GitLab Flow" based flow. PRs to main deploy to dev env. later stages can be accounted for by adding new "production/relese" branches and merging main into the newly added branches. release versions are created by humans tagging commits.
