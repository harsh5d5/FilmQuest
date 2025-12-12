# React Movies - Full Stack Application

## Project Structure

```
react-movies/
├── frontend (React + Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── MovieCard.jsx
│   │   │   ├── Search.jsx
│   │   │   └── Spinner.jsx
│   │   ├── services/
│   │   │   └── api.js          # Flask API integration
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   └── .env                    # Frontend environment variables
│
├── backend/ (Flask + Python)
│   ├── app.py                  # Main Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── movies.db              # SQLite database (auto-created)
│   ├── .env                   # Backend environment variables
│   └── README.md              # Backend documentation
│
└── start-dev.bat              # Windows startup script
```

## Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Hooks** - State management

### Backend
- **Flask** - Python web framework
- **SQLite** - Database for search history
- **TMDB API** - Movie data source
- **Flask-CORS** - Cross-origin requests

## Features Implemented

### ✅ Replaced Appwrite with Flask
- Movie search functionality
- Search history tracking
- Trending movies based on search count
- SQLite database for persistence

### ✅ API Endpoints
- `GET /api/movies` - Search/browse movies
- `POST /api/search-history` - Track searches
- `GET /api/trending` - Get popular searches
- `GET /api/health` - Health check

### ✅ Frontend Integration
- Service layer for API calls
- Error handling
- Loading states
- Real-time search with debouncing

## Running the Application

### Option 1: Manual Start
1. **Backend**: `cd backend && python app.py`
2. **Frontend**: `npm run dev`

### Option 2: Batch Script (Windows)
```bash
./start-dev.bat
```

## URLs
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:5000

## Environment Setup

### Backend (.env)
```
TMDB_API_KEY=your_tmdb_api_key_here
```

### Frontend (.env)
```
VITE_TMDB_API_KEY=your_tmdb_api_key_here  # Optional, not used with Flask backend
```