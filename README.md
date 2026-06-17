# NotesApp API

A backend-focused Notes API built with **FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication**.

This project allows users to register, log in, and manage their personal notes using protected REST API endpoints.

## Features

* User registration and login
* JWT-based authentication
* Password hashing using bcrypt
* Protected CRUD operations for notes
* User-specific notes access
* PostgreSQL database integration
* SQLAlchemy ORM models
* Pydantic request and response validation
* Modular backend structure with routers, schemas, models, CRUD layer, and database configuration
* Swagger API documentation for testing endpoints

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT
* Uvicorn
* Passlib / bcrypt

## Project Structure

```text
NotesApp/
│
├── core/
│   ├── auth.py
│   └── config.py
│
├── crud/
│   ├── note.py
│   └── user.py
│
├── db/
│   └── database.py
│
├── models/
│   ├── note.py
│   └── user.py
│
├── routers/
│   ├── auth.py
│   └── notes.py
│
├── schemas/
│   ├── note.py
│   └── user.py
│
├── main.py
├── requirements.txt
├── .env.example
└── runtime.txt
```

## API Endpoints

### Authentication

| Method | Endpoint         | Description                        |
| ------ | ---------------- | ---------------------------------- |
| POST   | `/auth/register` | Register a new user                |
| POST   | `/auth/login`    | Login and receive JWT access token |

### Notes

| Method | Endpoint           | Description                         |
| ------ | ------------------ | ----------------------------------- |
| GET    | `/notes/`          | Get all notes of the logged-in user |
| POST   | `/notes/`          | Create a new note                   |
| PUT    | `/notes/{note_id}` | Update an existing note             |
| DELETE | `/notes/{note_id}` | Delete a note                       |

## Local Setup

Clone the repository:

```bash
git clone https://github.com/codeash5/Notesapp.git
cd Notesapp
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root folder:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/notesapp
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Authentication Flow

1. Register a user using `/auth/register`.
2. Login using `/auth/login` or the Swagger **Authorize** button.
3. Use the JWT token to access protected note routes.
4. Create, view, update, and delete notes for the authenticated user.

## Deployment

The API is ready to deploy on platforms like Render or Railway.

Start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Completed features

Completed backend API with:

* JWT authentication
* Protected notes CRUD
* PostgreSQL database integration
* SQLAlchemy ORM
* Modular FastAPI architecture
* Swagger-based API testing
* Deployment-ready configuration

## Future Improvements

* Add Alembic migrations for production database version control
* Add refresh tokens
* Add pagination and search for notes
* Add unit tests
* Add Docker support
* Add rate limiting for authentication endpoints
