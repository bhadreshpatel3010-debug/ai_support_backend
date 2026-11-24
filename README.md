# AI Support Backend

Step-by-step guide and progress log for building the AI support backend.

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
├── docs/
├── requirements.txt
└── README.md
```

## Step 1: Project Setup

The project folder and Python environment are ready.

### Install Required Packages

The following dependencies were installed:

```powershell
pip install fastapi uvicorn sqlalchemy psycopg[binary] pgvector passlib[bcrypt] pyjwt python-dotenv google-genai
```

Main technologies:

- FastAPI — REST API framework
- Uvicorn — ASGI server
- SQLAlchemy — database ORM
- PostgreSQL + pgvector — database and vector storage
- Passlib + bcrypt — password hashing
- PyJWT — authentication tokens
- python-dotenv — environment variable management
- Google GenAI — AI model integration

## Step 2: Add Environment Variables

Create a `.env` file in the project root. Do not commit this file to Git.

```text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
JWT_SECRET_KEY=replace-with-a-long-random-secret
GOOGLE_API_KEY=replace-with-your-google-api-key
```

Example database name: `ai_support_db`.

## Step 3: Configure PostgreSQL

1. Install PostgreSQL.
2. Create a database for the project.
3. Enable the `pgvector` extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

4. Add the database URL to `.env`.

## Step 4: Database and Models

To be implemented in `app/database.py` and `app/models.py`:

- Configure the SQLAlchemy engine
- Create a database session
- Define database models
- Create tables at startup or through migrations
- Store embeddings using pgvector

## Step 5: Request and Response Schemas

Add Pydantic models in `app/schemas.py` for:

- Request validation
- Response serialization
- Authentication data
- Chat and support ticket data

## Step 6: Authentication

Add authentication in `app/auth.py`:

- Password hashing and verification
- User registration
- Login
- JWT creation
- JWT validation
- Protected route dependencies

## Step 7: RAG Service

Add retrieval-augmented generation logic in `app/rag_service.py`:

- Prepare and chunk documents
- Generate embeddings
- Save embeddings in pgvector
- Search for relevant documents
- Build a prompt with retrieved context
- Send the prompt to the Google GenAI model
- Return the generated answer

## Step 8: API Routes

Add API routes in `app/main.py`:

- Health check
- Authentication endpoints
- Document ingestion endpoints
- Question-answering endpoints
- Support ticket or conversation endpoints

## Step 9: Run the Server

Run the application from the project root:

```powershell
uvicorn app.main:app --reload
```

Open:

- API: http://127.0.0.1:8000
- Swagger documentation: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Step 10: Testing and Improvement

To be completed:

- Unit tests
- API integration tests
- Database migration setup
- Request logging
- Error handling
- CORS configuration
- Production deployment

## Progress Log

- [x] Created project structure
- [x] Installed core Python dependencies
- [ ] Added environment variables
- [ ] Configured PostgreSQL and pgvector
- [ ] Implemented database models
- [ ] Implemented authentication
- [ ] Implemented RAG service
- [ ] Added API routes
- [ ] Tested the application

## Development Notes

Add implementation decisions, commands, issues, fixes, and new features here as the project is developed.
