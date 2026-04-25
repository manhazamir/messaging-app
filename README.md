# MessagingApp (React + Django + WebSockets)

> Built in 2022 as a side-project in Django. Cleaned up and added a Readme later. 

- React (Create React App) frontend
- Django + Django REST Framework backend (token auth)
- Django Channels WebSockets for realtime chat and broadcasts
- Postgres as the database (configurable via environment variables)

## Features

- **Signup / Login** using DRF token authentication
- **Contacts** list (all registered users)
- **1:1 threads** between two users
- **Realtime chat** via WebSockets (messages are persisted)
- **Broadcast** websocket endpoint for sending a message to all connected users
- **Groups**: group model + API endpoints exist, but group websocket support is not finished

## Prerequisites

- Node.js + npm
- Python 3.10+ recommended
- Postgres running locally (or point to a remote instance)

## Quick start (Backend)

From the repo root:

```bash
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `server/.env` from the example:

```bash
copy .env.example .env
```

Edit `server/.env` and set at least:

- `DJANGO_SECRET_KEY`
- `POSTGRES_PASSWORD`

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Backend will be at `http://127.0.0.1:8000`.

## Quick start (Frontend)

In a new terminal:

```bash
cd messaging_app
copy .env.example .env
npm install
npm start
```

Frontend will be at `http://localhost:3000`.

## API + WebSocket endpoints

### REST

- `POST /signup/` – create user (returns token)
- `POST /login/` – login (returns token)
- `GET /get-contacts/` – list users
- `POST /thread/` – create/find thread between `user1` and `user2`
- `GET /messages/<userid>` – list threads + messages for a user
- `POST /new-group/` / `GET /get-groups/<userfk>` – group APIs

### WebSockets

- `ws://127.0.0.1:8000/ws/socket-server/?logged_user=<userId>`
  - Send payload:
    - `{ "message": "hi", "sent_by": 1, "send_to": 2, "thread_id": 3 }`
- `ws://127.0.0.1:8000/ws/broadcast-message/`

## Notes on configuration & security

  - `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
  - `DJANGO_CORS_ALLOWED_ORIGINS`
  - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`

