# Retrieval Augmented Generation (RAG) Service with FastAPI

This is a RAG Service in FastAPI.

## Notes

A collection of useful commands:

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

## CI/CD

"GitLab Flow" based flow. Push/PR to main should deploy to dev env. Each run of the pipeline builds, tests, increases semver patch version and pushes the image. After pushing the image, Helm deployment to EKS takes place. Deployments to other environment can be accounted for by adding new "production/relese" branches and merging main into the newly added branches.

### Setup

In `.github/workflows`, there are GitHub Action workflows that build and test the app on push to `main`. Upon successfull tests, the CI/CD increases the semver of the app and triggers a build and push to the `ghcr.io` registry. After this, the app is deployed with Helm to the EKS cluster. For the GitHub CI/CD to run, a deploment environment and according secrets/variables have to be created.

- Create your own `.env.dev` file from `.env.dist`
- run `poetry run python .github/create_github_env.py`
- Push changes to the repo and watch the pipeline run. Good luck.

Hint: poetry install caching not working properly, so pipeline runs are quite slow currently
