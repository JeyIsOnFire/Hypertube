"use client";

import React, { useState, useEffect, use } from 'react';
import { useParams } from 'react-router-dom';
import { fetchApi } from '../../components/fetch-api';
import styles from './filmPage.module.css'; // ou ton fichier CSS global

export default function FilmPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);

  const [movieData, setMovieData] = useState(null);

  useEffect(() => {
    const fetchPopularMovies = async () => {
      try {
        const res = await fetchApi(`getMovieInfosById/${id}`);
        setMovieData(res);
      } catch (err) {
        console.error("Erreur API: ", err);
      }
    };
    fetchPopularMovies();
  }, [id]);


  return (
    <div>
      <div>

        {/* Contenu du film */}
        {movieData && (
          <main className={styles.hero}>
            <h2>{movieData.original_title}</h2>
            <img src={"https://image.tmdb.org/t/p/w300" + movieData.poster_path} alt={`Affiche de ${movieData.original_title}`} style={{ width: '100%', maxWidth: '300px', borderRadius: '4px', marginBottom: '1rem' }} />
            <p style={{ maxWidth: '600px', margin: '0 auto 1.5rem' }}>{movieData.overview}</p>
            <ul style={{ listStyle: 'none', padding: 0, textTransform: 'uppercase', fontFamily: 'var(--ff-heading)' }}>
              <li><strong>Genre :</strong> {movieData.genres[0].name}</li>
              <li><strong>Durée :</strong> {movieData.runtime} min</li>
              <li><strong>Année :</strong> {movieData.release_date}</li>
            </ul>
            <button>Regarder maintenant</button>
          </main>
        )}

        {/* Footer */}
      </div>

      {movieData ? (
        <pre>{JSON.stringify(movieData, null, 2)}</pre>
      ) : (
        "Chargement..."
      )}
    </div>
  );
}

