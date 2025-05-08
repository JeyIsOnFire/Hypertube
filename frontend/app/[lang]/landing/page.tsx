"use client";

import React, { use, useState, useEffect } from 'react';
import styles from './landing.module.css';
import Link from 'next/link';
import { fetchApi } from '@/lib/fetch-api';
import translations from '@/locales';



const Landing: React.FC = ({ params }: { params: { lang: string }}) => {

  const lang = use(params).lang;
  const [response, setReponse] = useState(null); 
  const t = translations[lang];
  if (!t) {
    console.error(`Missing translations for lang: ${lang}`);
    return null;
  }
  const [popularFilms, setPopularFilms] = useState([]);

  useEffect(() => {
    const fetchPopularMovies = async () => {
      try {
        const res = await fetchApi(`fetchPopularMovies`);
        setPopularFilms(res);
      } catch (err) {
        console.error("Erreur API: ", err);
      }
    };
    fetchPopularMovies();
  }, []);

  return (
    <>

      {/*----------------------------- SEARCH BAR -----------------------------*/}
      {response && (() => {
        const parsed = JSON.parse(response)['results'];
        console.log("JSON", parsed);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return (
            <div className={styles.results}>
              <div className={styles.filmList}>
                {parsed.slice(0, 10).map((film: any, index: number) => (
                  <Link
                    key={index}
                    href={`/films/${film['id']}`}
                    className={styles.filmCard}
                  >
                    <h3>{film['title']}</h3>
                    <p>{film['release_date']}</p>
                  </Link>
                ))}
              </div>
            </div>
          );
        } else {
          return (
            <div className={styles.results}>
              <div className={styles.filmList}>
                <div className={`${styles.filmCard}`}>{t.noresults}</div>;
              </div>
            </div>
          )
        }
      })()}

      {/*----------------------------- ENTER THE HYPERTUBE -----------------------------*/}
      <section className={styles.hero}>
        <h2>{t.searchformovies}</h2>
        <button>{t.enterhypertube}</button>
      </section>

      {/*----------------------------- POPULAR FILMS -----------------------------*/}
      <section className={styles.grid}>
        {popularFilms.results?.map((film) => (
          <div key={film.id} className={styles.card}>
            <img src={`https://image.tmdb.org/t/p/w300${film.poster_path}`} alt={film.title} />
            <div className={styles.info}>
              <h3>{film.title}</h3>
              <p>{film.release_date.slice(0, 4)}</p>
            </div>
          </div>
        ))}
      </section>


      {popularFilms && (
        <div>{JSON.stringify(popularFilms)}</div>
      )}

    </>
  );
}

export default Landing;

