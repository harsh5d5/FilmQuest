import React, { useState, useEffect } from 'react'

const TopMoviesSlider = ({ movies }) => {
  const [currentIndex, setCurrentIndex] = useState(0)

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === movies.length - 1 ? 0 : prevIndex + 1
    )
  }

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === 0 ? movies.length - 1 : prevIndex - 1
    )
  }

  // Auto-slide every 5 seconds
  useEffect(() => {
    const interval = setInterval(nextSlide, 5000)
    return () => clearInterval(interval)
  }, [movies.length])

  if (!movies || movies.length === 0) return null

  return (
    <section className="top-movies-slider">
      <h2>Trending Now</h2>
      
      <div className="slider-container">
        <button className="slider-btn prev" onClick={prevSlide}>
          ‹
        </button>
        
        <div className="slider-wrapper">
          <div 
            className="slider-track"
            style={{ transform: `translateX(-${currentIndex * (100 / Math.min(movies.length, 6))}%)` }}
          >
            {movies.slice(0, 10).map((movie, index) => (
              <div key={movie.id} className="slider-item">
                <div className="movie-rank">
                  <span className="rank-number">{index + 1}</span>
                </div>
                <div className="movie-poster">
                  <img
                    src={movie.poster_path && movie.poster_path !== 'N/A' ? movie.poster_path : '/no-movie.png'}
                    alt={movie.title}
                    onError={(e) => {
                      e.target.src = '/no-movie.png'
                    }}
                  />
                </div>
                <div className="movie-info">
                  <h3>{movie.title}</h3>
                  <p className="movie-year">{movie.release_date}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <button className="slider-btn next" onClick={nextSlide}>
          ›
        </button>
      </div>
      
      <div className="slider-dots">
        {Array.from({ length: Math.ceil(movies.length / 6) }).map((_, index) => (
          <button
            key={index}
            className={`dot ${index === Math.floor(currentIndex / 6) ? 'active' : ''}`}
            onClick={() => setCurrentIndex(index * 6)}
          />
        ))}
      </div>
    </section>
  )
}

export default TopMoviesSlider