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
    - docker build --progress=plain --no-cache --platform linux/amd64 -t ghcr.io/acn-catwalk-llmops/service-rag:0.0.1 .
    - docker build --platform linux/amd64 -t ghcr.io/acn-catwalk-llmops/service-rag:0.0.1 .
  - docker run -p 8000:8000 service-rag
  - login to GitHub container registry
    - export CR_TOKEN={YOUR_GH_TOKEN}
    - echo $CR_TOKEN | docker login ghcr.io -u {YOUR_GH_USERNAME_NOT_EMAIL} --password-stdin
  - docker push ghcr.io/acn-catwalk-llmops/service-rag:0.0.1
- Precommit:
  - pre-commit install
  - pre-commit run --all-files
- Test:
  - poetry run pytest .
  - docker build -t ghcr.io/acn-catwalk-llmops/service-rag:test . --target test
  - docker run ghcr.io/acn-catwalk-llmops/service-rag:test

- Helm
  - helm install service-rag helm/service-rag
  - helm uninstall service-rag
  - helm template helm/service-rag
- Git tag and push tag
  - git tag v1.2.3
  - git push origin v1.2.3

## TODOs

- App
  - test document loader
  - evtl andere vector datenbank integrieren und probieren zu abstrahieren
- CICD
  - make application ports configurable?

## CI

"GitLab Flow" based flow. Push/PR to main should deploy to dev env. Each run of the pipeline builds, tests, increases semver patch version and pushes the image. After pushing the image, Helm deployment to EKS takes place. Deployments to other environment can be accounted for by adding new "production/relese" branches and merging main into the newly added branches.

### Github Actions Setup

-
-
