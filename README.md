![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.


# 🎵 Sound Mood Detector

A containerized full-stack application that listens to microphone input, uses machine learning to detect the user's **mood**, and displays results on a web dashboard.

---

## Project Structure

This monorepo contains three subsystems:

| Folder                   | Description                                         |
|--------------------------|-----------------------------------------------------|
| `machine-learning-client` | Captures audio, performs ML analysis, stores results in MongoDB |
| `web-app`                | Flask dashboard that visualizes results            |
| `mongodb`                | MongoDB container using the official image         |

---



## Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/)
- [pipenv](https://pipenv.pypa.io/en/latest/)
  ```bash
  pip install pipenv
  ```
- Docker Desktop
- Git



## RUnning the Full App with Docker Compose

Make sure you’re in the root of the project (4-containers-bravo/), then:

```bash
docker compose up --build
```

This will start:
    - ML client (machine-learning-client/)
	- Flask web app (web-app/)
	- MongoDB

To stop:

```bash
docker compose down
```



## Local Development

Run the ML Client Locally:

```bash
cd machine-learning-client
pipenv install
pipenv run python main.py
```

Run the Web App Locally

```bash
cd web-app
pip install -r requirements.txt
python app.py
```



## Environment Variables

1. Setup
Create a .env file in the project root:

```bash
cp .env.example .env
```

Edit .env with your own values.



2. Mongo URI
MongoDB will be accessible from inside Docker containers via:

```bash
mongodb://mongodb:27017
```
This is already set via the docker-compose.yml file for both services.



## CI/CD & Code Quality
	- Python code is linted with pylint
	- Automatically formatted with black
	- GitHub Actions CI runs checks on every push/pull request
	= pipenv is used for managing dependencies in machine-learning-client



## Contributors
    - [@TimYan] (https://github.com/T1mmmmm)
    - [@lawaldemur](https://github.com/lawaldemur) Vladimir Kartamyshev
    -
    -



## Repository
https://github.com/software-students-spring2025/4-containers-bravo
