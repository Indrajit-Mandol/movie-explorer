# 🎬 CineScope — Movie Explorer Platform

A full-stack movie browsing application built with **Flask** (backend) and **React + TypeScript** (frontend). Browse movies, explore actor and director profiles, filter by genre/year/director/actor, and save favorites.

---

## Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Backend   | Python, FastAPI, SQLAlchemy, SQLite     |
| API Docs  | FastAPI built-in (Swagger + ReDoc)      |
| Frontend  | React 18, TypeScript, Vite              |
| Styling   | Custom CSS (no framework dependencies)  |
| Testing   | pytest (backend), Vitest + RTL (frontend) |
| Deploy    | Docker + Docker Compose                 |

---

## Project Structure

```
movie-explorer/
├── backend/
│   ├── main.py             # FastAPI app, CORS, lifespan (DB seed on startup)
│   ├── database.py         # SQLAlchemy engine, session, get_db dependency
│   ├── models.py           # SQLAlchemy models (Movie, Actor, Director, Genre)
│   ├── schemas.py          # Pydantic schemas for request/response validation
│   ├── seed_data.py        # DB seeder with ~20 sample movies
│   ├── routers/
│   │   ├── movies.py       # GET /api/movies/, GET /api/movies/{id}
│   │   ├── actors.py       # GET /api/actors/, GET /api/actors/{id}
│   │   ├── directors.py    # GET /api/directors/, GET /api/directors/{id}
│   │   └── genres.py       # GET /api/genres/, GET /api/genres/{id}
│   ├── tests/
│   │   └── test_api.py     # 30+ pytest tests using FastAPI TestClient
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pytest.ini
│
├── frontend/
│   ├── src/
│   │   ├── api/client.ts       # API calls with query builder
│   │   ├── components/         # Reusable UI components
│   │   ├── hooks/              # useFetch, useFavorites
│   │   ├── pages/              # Route-level page components
│   │   ├── types/index.ts      # TypeScript interfaces
│   │   ├── App.tsx             # Router setup
│   │   ├── main.tsx            # Entry point
│   │   └── index.css           # Global styles (cinema dark theme)
│   ├── src/test/
│   │   └── components.test.tsx # 15+ Vitest unit tests
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
└── README.md
```

---

## Quick Start with Docker (Recommended)

**Prerequisites**: Docker and Docker Compose installed.

```bash
# 1. Clone the repository
git clone https://github.com/Indrajit-Mandol/movie-explorer.git
cd movie-explorer

# 2. Build and start both services
docker-compose up --build

# 3. Open the app
# Frontend: http://localhost:3000
# API Docs: http://localhost:5000/api/docs/
```

To stop:
```bash
docker-compose down
```

To wipe data and restart fresh:
```bash
docker-compose down -v
docker-compose up --build
```

---

## Local Development (Without Docker)

### Backend

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server (creates and seeds DB automatically on first run)
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
# → Running on http://localhost:5000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server (proxies /api to localhost:5000)
npm run dev
# → Running on http://localhost:3000
```

---

## Running Tests

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

Tests cover:
- Movie listing and filtering (genre, director, actor, year, title search)
- Edge cases: invalid filters, non-existent IDs, empty results
- Actor/Director profile endpoints
- Genre listing
- HTTP error codes (400, 404)

### Frontend Tests

```bash
cd frontend
npm install
npm test
```

Tests cover:
- `MovieCard` — renders title, rating, genres, navigates on click
- `PersonCard` — renders actor/director info, navigates correctly
- `EmptyState`, `LoadingState` — render correctly
- `useFavorites` hook — add, remove, persist to localStorage

---

## API Documentation

FastAPI auto-generates interactive API docs — no extra configuration needed:

| UI      | URL                              |
|---------|----------------------------------|
| Swagger | **http://localhost:5000/api/docs**   |
| ReDoc   | **http://localhost:5000/api/redoc**  |
| OpenAPI JSON | http://localhost:5000/api/openapi.json |

### Endpoints Summary

| Method | Endpoint                     | Description                         |
|--------|------------------------------|-------------------------------------|
| GET    | `/api/health`                | Health check                        |
| GET    | `/api/movies/`               | List movies (supports filters)      |
| GET    | `/api/movies/<id>`           | Movie detail with full cast         |
| GET    | `/api/actors/`               | List actors (supports filters)      |
| GET    | `/api/actors/<id>`           | Actor profile with filmography      |
| GET    | `/api/directors/`            | List directors                      |
| GET    | `/api/directors/<id>`        | Director profile with filmography   |
| GET    | `/api/genres/`               | List all genres                     |
| GET    | `/api/genres/<id>`           | Genre detail                        |

### Movie Filter Parameters

| Parameter     | Type    | Description                        |
|---------------|---------|------------------------------------|
| `genre_id`    | integer | Filter by genre                    |
| `director_id` | integer | Filter by director                 |
| `actor_id`    | integer | Filter by actor                    |
| `release_year`| integer | Filter by exact year (1888–2100)   |
| `search`      | string  | Partial title match (case-insensitive) |

**All filtering is handled on the backend.**

### Example Requests

```bash
# All movies
curl http://localhost:5000/api/movies/

# Filter by genre
curl "http://localhost:5000/api/movies/?genre_id=1"

# Filter by director + year
curl "http://localhost:5000/api/movies/?director_id=1&release_year=2010"

# Search by title
curl "http://localhost:5000/api/movies/?search=inception"

# Actor profile
curl http://localhost:5000/api/actors/1
```

---

## Data Model

```
Genre ─────┐
           ├─── (many-to-many) ──► Movie ◄── (many-to-one) ── Director
Actor ─────┘ (many-to-many)
```

- A **Movie** belongs to multiple **Genres**
- A **Movie** has multiple **Actors**
- A **Movie** has one **Director**
- **Movies** include a **rating** (out of 10, representative of real-world ratings)

---

## Features

- ✅ Browse movies with title, year, rating, genres, director
- ✅ Filter movies by genre, director, actor, release year, or title
- ✅ Movie detail page with full cast and synopsis
- ✅ Actor profile with filmography and genre breakdown
- ✅ Director profile with filmography and average rating
- ✅ Swagger UI for API documentation
- ✅ Unit tests for backend (pytest) and frontend (Vitest)
- ✅ Dockerized with docker-compose
- ✅ Linting integrated into the build step
- ✅ **Bonus**: Favorites / Watch Later (localStorage, no account needed)

---

## Edge Cases Handled

| Scenario                         | Behavior                                  |
|----------------------------------|-------------------------------------------|
| Filter by non-existent genre ID  | Returns HTTP 404 with error detail        |
| Filter by invalid year (< 1888)  | Returns HTTP 422 (FastAPI validation)     |
| Search with no matches           | Returns `{ movies: [], count: 0, message }` |
| Movie ID not found               | Returns HTTP 404                          |
| Actor/Director not found         | Returns HTTP 404                          |
| Empty database                   | Returns empty arrays with message         |
| Network error in frontend        | Displays error state with retry button    |
| No favorites saved               | Shows empty state with instructions       |

---

## Environment Variables

| Variable       | Default                        | Description                  |
|----------------|--------------------------------|------------------------------|
| `DATABASE_URL` | `sqlite:///movie_explorer.db`  | SQLAlchemy DB connection URL |
| `SECRET_KEY`   | `dev-secret-key`               | Flask secret key             |
