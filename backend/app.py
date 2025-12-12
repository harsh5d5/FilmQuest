from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime
import sqlite3
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
OMDB_API_KEY = os.getenv('OMDB_API_KEY', '73de91ff')
OMDB_BASE_URL = 'https://www.omdbapi.com'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    # Create search_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_term TEXT NOT NULL,
            movie_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            poster_url TEXT,
            count INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# OMDB API helper
def get_omdb_params(additional_params=None):
    params = {'apikey': OMDB_API_KEY}
    if additional_params:
        params.update(additional_params)
    return params

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Get movies from OMDB API"""
    query = request.args.get('query', '')
    
    try:
        if query:
            # Search movies by title
            params = get_omdb_params({'s': query, 'type': 'movie'})
            response = requests.get(OMDB_BASE_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    # Convert OMDB format to our expected format
                    movies = []
                    for movie in data.get('Search', []):
                        movies.append({
                            'id': movie.get('imdbID'),
                            'title': movie.get('Title'),
                            'poster_path': movie.get('Poster') if movie.get('Poster') != 'N/A' else None,
                            'release_date': movie.get('Year'),
                            'original_language': 'en',  # OMDB doesn't provide this
                            'vote_average': 'N/A'  # OMDB doesn't provide this in search
                        })
                    
                    return jsonify({
                        'success': True,
                        'results': movies
                    })
                else:
                    return jsonify({
                        'success': True,
                        'results': []
                    })
        else:
            # OMDB doesn't have a "popular movies" endpoint, so return some default popular movies
            popular_movies = ['Inception', 'The Dark Knight', 'Pulp Fiction', 'The Godfather', 'Forrest Gump']
            all_movies = []
            
            for movie_title in popular_movies:
                params = get_omdb_params({'t': movie_title})
                movie_response = requests.get(OMDB_BASE_URL, params=params)
                
                if movie_response.status_code == 200:
                    movie_data = movie_response.json()
                    if movie_data.get('Response') == 'True':
                        all_movies.append({
                            'id': movie_data.get('imdbID'),
                            'title': movie_data.get('Title'),
                            'poster_path': movie_data.get('Poster') if movie_data.get('Poster') != 'N/A' else None,
                            'release_date': movie_data.get('Year'),
                            'original_language': movie_data.get('Language', 'en').split(',')[0].lower(),
                            'vote_average': movie_data.get('imdbRating', 'N/A')
                        })
            
            return jsonify({
                'success': True,
                'results': all_movies
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search-history', methods=['POST'])
def update_search_count():
    """Update search count for a movie"""
    data = request.get_json()
    search_term = data.get('search_term')
    movie = data.get('movie')
    
    if not search_term or not movie:
        return jsonify({'success': False, 'error': 'Missing required data'}), 400
    
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        # Check if search term exists
        cursor.execute(
            'SELECT id, count FROM search_history WHERE search_term = ? AND movie_id = ?',
            (search_term, movie['id'])
        )
        result = cursor.fetchone()
        
        if result:
            # Update existing record
            cursor.execute(
                'UPDATE search_history SET count = count + 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (result[0],)
            )
        else:
            # Create new record - OMDB provides full poster URLs
            poster_url = movie.get('poster_path') if movie.get('poster_path') and movie.get('poster_path') != 'N/A' else None
            cursor.execute(
                '''INSERT INTO search_history (search_term, movie_id, title, poster_url, count)
                   VALUES (?, ?, ?, ?, 1)''',
                (search_term, movie['id'], movie['title'], poster_url)
            )
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/trending', methods=['GET'])
def get_trending_movies():
    """Get trending movies from search history"""
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        cursor.execute(
            '''SELECT search_term, movie_id, title, poster_url, count
               FROM search_history
               ORDER BY count DESC, updated_at DESC
               LIMIT 5'''
        )
        
        results = cursor.fetchall()
        conn.close()
        
        trending_movies = []
        for row in results:
            trending_movies.append({
                'id': row[1],
                'search_term': row[0],
                'title': row[2],
                'poster_url': row[3],
                'count': row[4]
            })
        
        return jsonify({
            'success': True,
            'results': trending_movies
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/top-movies', methods=['GET'])
def get_top_movies():
    """Get top 10 popular movies"""
    try:
        # List of popular movies to fetch
        top_movie_titles = [
            'The Shawshank Redemption',
            'The Godfather',
            'The Dark Knight',
            'Pulp Fiction',
            'Forrest Gump',
            'Inception',
            'The Matrix',
            'Goodfellas',
            'The Lord of the Rings: The Return of the King',
            'Fight Club'
        ]
        
        top_movies = []
        
        for movie_title in top_movie_titles:
            params = get_omdb_params({'t': movie_title})
            response = requests.get(OMDB_BASE_URL, params=params)
            
            if response.status_code == 200:
                movie_data = response.json()
                if movie_data.get('Response') == 'True':
                    top_movies.append({
                        'id': movie_data.get('imdbID'),
                        'title': movie_data.get('Title'),
                        'poster_path': movie_data.get('Poster') if movie_data.get('Poster') != 'N/A' else None,
                        'release_date': movie_data.get('Year'),
                        'original_language': movie_data.get('Language', 'en').split(',')[0].lower(),
                        'vote_average': movie_data.get('imdbRating', 'N/A'),
                        'plot': movie_data.get('Plot', ''),
                        'genre': movie_data.get('Genre', ''),
                        'director': movie_data.get('Director', '')
                    })
        
        return jsonify({
            'success': True,
            'results': top_movies
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)