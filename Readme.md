# Subscription Management Backend

A scalable, production-ready backend built with **FastAPI**, **PostgreSQL**,
**SQLAlchemy**, **Redis**, and **Celery** to manage user subscriptions and plan
lifecycles.

## Deployed Demo

Access the live API at:
[http://ec2-13-201-98-2.ap-south-1.compute.amazonaws.com](http://ec2-13-201-98-2.ap-south-1.compute.amazonaws.com)

> **Note:** If you get a "connection refused" error, ensure you are accessing the API via **http** and not **https**.

## API Documentation

For detailed API endpoints and schemas, visit the interactive Swagger docs at:
[http://ec2-13-201-98-2.ap-south-1.compute.amazonaws.com/docs](http://ec2-13-201-98-2.ap-south-1.compute.amazonaws.com/docs)


## Features

-   JWT Authentication (Login/Signup)
-   Role-Based Access Control (Admin/User)
-   Create, Update, Cancel Subscriptions
-   Subscription Expiry handled by Celery Beat
-   Admin-only Plan Management (Create/Update/Delete Plans)
-   Full Test Suite with `pytest` and `httpx`
-   Retry Logic on DB Failures (`tenacity`)
-   Async support throughout
-   Modular, maintainable project structure

---

## Tech Stack

-   **FastAPI** - Async API framework
-   **PostgreSQL** - Main relational database
-   **SQLAlchemy** - Async ORM
-   **Alembic** - DB migrations
-   **Pydantic** - Schema validation
-   **Celery + Redis** - Background tasks & task queue
-   **Docker** - Containerization
-   **Pytest** - Testing framework

---

## Project Structure

```
app/
├── auth/               # JWT Auth handlers & dependencies
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
├── routers/            # FastAPI routers
├── services/           # Business logic
├── tasks/              # Celery tasks (e.g. subscription expiry)
├── utils/              # Helpers like retry logic
├── database.py         # Async engine and session
├── main.py             # Entry point
celery_worker.py        # Celery worker instance
alembic/                # DB migrations
tests/                  # Tests
```

---

## Running Tests

```bash
pytest
```

---

## Setup Instructions

```bash
# Clone the repo
$ git clone https://github.com/CodeWithDevesh/Subscription-Service
$ cd Subscription-Service

# Setup virtual environment
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

# Run DB migrations
$ alembic upgrade head

# Start Redis server (Docker recommended)
$ docker run -p 6379:6379 redis

# Start FastAPI app
$ uvicorn app.main:app --reload

# Start Celery worker
$ celery -A celery_worker.celery_app worker --loglevel=info

# Start Celery beat for periodic tasks
$ celery -A celery_worker.celery_app beat --loglevel=info
```

---

## Future Improvements

-   Rate Limiting (`slowapi`)
-   Swagger Auth for `/docs`
-   Subscription emails (welcome, renewal, expiry notifications)

---
