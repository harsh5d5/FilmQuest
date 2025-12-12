const API_BASE_URL = 'http://localhost:5000/api';

// Fetch movies from Flask backend
export const fetchMoviesFromAPI = async (query = '') => {
  try {
    const url = query 
      ? `${API_BASE_URL}/movies?query=${encodeURIComponent(query)}`
      : `${API_BASE_URL}/movies`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.success) {
      return data.results;
    } else {
      throw new Error(data.error || 'Failed to fetch movies');
    }
  } catch (error) {
    console.error('Error fetching movies:', error);
    throw error;
  }
};

// Update search count in Flask backend
export const updateSearchCount = async (searchTerm, movie) => {
  try {
    const response = await fetch(`${API_BASE_URL}/search-history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        search_term: searchTerm,
        movie: movie
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to update search count');
    }
    
    return data;
  } catch (error) {
    console.error('Error updating search count:', error);
    throw error;
  }
};

// Get trending movies from Flask backend
export const getTrendingMovies = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/trending`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.success) {
      return data.results;
    } else {
      throw new Error(data.error || 'Failed to fetch trending movies');
    }
  } catch (error) {
    console.error('Error fetching trending movies:', error);
    throw error;
  }
};

// Get top 10 movies from Flask backend
export const getTopMovies = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/top-movies`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.success) {
      return data.results;
    } else {
      throw new Error(data.error || 'Failed to fetch top movies');
    }
  } catch (error) {
    console.error('Error fetching top movies:', error);
    throw error;
  }
};