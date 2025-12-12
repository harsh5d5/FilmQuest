# Flask Backend for React Movies

This Flask backend replaces the Appwrite functionality with a Python-based API.

## Features

- **Movie Search**: Fetches movies from OMDB API
- **Search History**: Tracks search terms and counts using SQLite
- **Trending Movies**: Returns most searched movies
- **CORS Support**: Configured for React frontend

## Setup

### 1. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file:
```bash
OMDB_API_KEY=your_omdb_api_key_here
```

### 3. Run the Server

```bash
python app.py
```

The server will run on `http://localhost:5000`

## API Endpoints

### GET /api/movies
- **Description**: Get movies from OMDB
- **Parameters**: 
  - `query` (optional): Search term
- **Response**: List of movies

### POST /api/search-history
- **Description**: Update search count for a movie
- **Body**: 
  ```json
  {
    "search_term": "batman",
    "movie": { "id": 123, "title": "Batman", "poster_path": "/path.jpg" }
  }
  ```

### GET /api/trending
- **Description**: Get trending movies from search history
- **Response**: List of most searched movies

### GET /api/health
- **Description**: Health check endpoint
- **Response**: Server status

## Database

Uses SQLite database (`movies.db`) to store:
- Search history
- Movie search counts
- Trending data

## CORS

Configured to allow requests from React frontend running on `http://localhost:5173`