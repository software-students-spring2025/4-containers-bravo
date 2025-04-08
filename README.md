![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.


## Prerequisites

Before running this project locally, make sure you have the following installed:

- Python 3.10+
- [Pipenv](https://pipenv.pypa.io/en/latest/)

Install pipenv (if not installed):

```bash
pip install pipenv

```

## Running the ML Client with Docker (Standalone)

Make sure you are inside the `machine-learning-client/` directory:

```bash
cd machine-learning-client
docker build -t sound-mood-client .
docker run sound-mood-client

```

## Quit docker
Ctrl + c in terminal, then:
```bash
docker compose down
```