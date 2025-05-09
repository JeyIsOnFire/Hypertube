"use client";

import React, { use, useState, useEffect } from 'react';
import styles from './landing.module.css';
import Link from 'next/link';
import { fetchApi } from '@/lib/fetch-api';
import translations from '@/locales';



const Landing: React.FC = ({ params }: { params: { lang: string }}) => {

  const lang = use(params).lang;
  const t = translations[lang];
  if (!t) {
    console.error(`Missing translations for lang: ${lang}`);
    return null;
  }

  const [popularFilms, setPopularFilms] = useState([]);
  const [pageNum, setPageNum] = useState<number>(1);

  useEffect(() => {
    const fetchPopularMovies = async () => {
      try {
        const res = await fetchApi(`fetchPopularMovies/${pageNum}`);
        console.log("res:", res);
        setPopularFilms(prev => [...prev, ...res['results']]);
        console.log("popular:", popularFilms);
      } catch (err) {
        console.error("Erreur API: ", err);
      }
    };
    fetchPopularMovies();
  }, [pageNum]);

  const getColorFromNote = (note) => {
    const clampedNote = Math.max(0, Math.min(parseInt(note), 10)); 
    const hue = (clampedNote / 10) * 120;
    return `hsl(${hue}, 100%, 30%)`;
  }

  const handleScroll = () => {
    const scrollTop = window.scrollY;
    const winH = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    if (scrollTop + winH >= docHeight - 50) {
      setPageNum(prev => prev + 1);
      console.log("Bas de page");
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  });

  return (
    <>
      {/*----------------------------- ENTER THE HYPERTUBE -----------------------------*/}
      <section className={styles.hero}>
        <h2>{t.searchformovies}</h2>
        <button>{t.enterhypertube}</button>
      </section>

      {/*----------------------------- POPULAR FILMS -----------------------------*/}
      <section className={styles.grid}>
        {popularFilms?.map((film, index: number) => (
          <div key={film.id} className={styles.card}>
            <Link
              onClick={()=>setResponse(null)}
              key={index}
              href={`/films/${film['id']}`}
            >
              <div className={styles.info}>
                <img src={`https://image.tmdb.org/t/p/w300${film.poster_path}`} alt={film.title} />
                <div style={{ padding: '0.2rem' }}>
                  <h3>{film.title}</h3>
                  <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
                    <p>{film.release_date.slice(0, 4)}</p>
                    <p><span style={{ color: getColorFromNote(film.vote_average)}}>{film.vote_average}</span>/10</p>
                  </div> 
                </div>
              </div> 
            </Link >
          </div>
        ))}
      </section>



    </>
  );
}

export default Landing;

