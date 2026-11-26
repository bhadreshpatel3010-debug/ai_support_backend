# AI Support Backend

A FastAPI-based customer support backend that uses PostgreSQL with pgvector for semantic knowledge search and the Google Gemini API for generated answers.

## Features

- User registration and password hashing
- Login with JWT bearer authentication
- PostgreSQL database initialization
- pgvector document embeddings
- Paragraph-based knowledge ingestion
- Semantic retrieval of relevant knowledge chunks
- Chat history stored per authenticated user
- Grounded Gemini responses using retrieved company knowledge
- Interactive Swagger and ReDoc API documentation

## Project Structure

```text
ai_support_backend/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── rag_service.py
│   └── schemas.py
├── README.md
└── requirements.txt
```

## Technology Stack

- FastAPI and Uvicorn
- SQLAlchemy
- PostgreSQL and pgvector
- Passlib and bcrypt
- PyJWT
- Pydantic
- Google GenAI SDK
- python-dotenv

## Prerequisites

- Python 3.10 or newer
- PostgreSQL
- pgvector installed for the PostgreSQL server
- A Google Gemini API key

## Installation

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root. Do not commit this file to Git.

```text
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/ai_support_db
SECRET_KEY=replace-with-a-long-random-secret
GEMINI_API_KEY=replace-with-your-gemini-api-key
```

These variable names match [app/database.py](app/database.py), [app/auth.py](app/auth.py), and [app/rag_service.py](app/rag_service.py).

## PostgreSQL Setup

Create a database named `ai_support_db`. The application enables the pgvector extension and creates tables when it starts:

```sql
CREATE DATABASE ai_support_db;
CREATE EXTENSION IF NOT EXISTS vector;
```

The database models define:

- `users` — account email and hashed password
- `document_chunks` — knowledge text and 768-dimensional Gemini embeddings
- `chat_history` — user and assistant conversation messages

## Run the API

Start the server from the project root:

```powershell
uvicorn app.main:app --reload
```

Open:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| `POST` | `/register` | None | Register a user |
| `POST` | `/login` | None | Log in using form fields `username` and `password` |
| `POST` | `/ingest` | Bearer token | Split text into paragraphs and store embeddings |
| `POST` | `/chat` | Bearer token | Retrieve relevant knowledge and generate a support reply |

Authenticated endpoints require:

```text
Authorization: Bearer <access_token>
```

## Usage Example

Register a user:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/register" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"support@example.com","password":"change-this-password"}'
```

Log in using OAuth2 form fields:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/login" `
  -Method Post `
  -Body @{ username = "support@example.com"; password = "change-this-password" }
```

Use the returned token for protected requests:

```powershell
$token = "<access-token>"
$headers = @{ Authorization = "Bearer $token" }

Invoke-RestMethod -Uri "http://127.0.0.1:8000/ingest" `
  -Method Post `
  -Headers $headers `
  -ContentType "application/json" `
  -Body '{"text":"Our support hours are Monday through Friday, 9 AM to 5 PM.`n`nReturns are accepted within 30 days of purchase."}'

Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" `
  -Method Post `
  -Headers $headers `
  -ContentType "application/json" `
  -Body '{"message":"What are the support hours?"}'
```

## How the RAG Flow Works

1. Knowledge text is split into paragraphs.
2. Gemini `text-embedding-004` creates a 768-dimensional embedding for each paragraph.
3. Document embeddings are stored in PostgreSQL using pgvector.
4. A chat question is converted into an embedding.
5. The three closest document chunks are retrieved by cosine distance.
6. Recent chat history is added to the prompt.
7. Gemini `gemini-2.5-flash` generates a grounded support answer.
8. The question and response are saved to chat history.

## Implementation Status

- [x] FastAPI application and lifespan initialization
- [x] PostgreSQL and pgvector setup
- [x] SQLAlchemy models
- [x] Pydantic request and response schemas
- [x] User registration and login
- [x] JWT authentication
- [x] Knowledge ingestion
- [x] Embedding-based retrieval
- [x] Gemini support responses
- [x] Per-user chat history
- [ ] Automated tests
- [ ] Database migrations
- [ ] Structured logging and monitoring
- [ ] CORS configuration
- [ ] Production deployment configuration

## Development Notes

- Passwords are hashed with bcrypt through Passlib.
- JWTs expire after 60 minutes.
- The current chunking strategy separates text by blank lines (`\n\n`).