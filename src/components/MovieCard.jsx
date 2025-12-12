import React from 'react'

const MovieCard = ({ movie:
  { title, vote_average, poster_path, release_date, original_language }
}) => {
  return (
    <div className="movie-card">
      <img
        src={poster_path && poster_path !== 'N/A' ? poster_path : '/no-movie.png'}
        alt={title}
      />

      <div className="mt-4">
        <h3>{title}</h3>

        <div className="content">
          <div className="rating">
            <img src="star.svg" alt="Star Icon" />
            <p>{vote_average && vote_average !== 'N/A' ? (typeof vote_average === 'number' ? vote_average.toFixed(1) : vote_average) : 'N/A'}</p>
          </div>

          <span>•</span>
          <p className="lang">{original_language}</p>

          <span>•</span>
          <p className="year">
            {release_date ? (release_date.includes('-') ? release_date.split('-')[0] : release_date) : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  )
}
export default MovieCard
