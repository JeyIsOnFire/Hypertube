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
  const [isFetching, setIsFetching] = useState(false);

  useEffect(() => {
    const debounce = setTimeout(() => {
      const fetchPopularMovies = async () => {
        try {
          console.log("page num:", pageNum);
          const res = await fetchApi(`${lang}/fetchPopularMovies/${pageNum}`);

          const newFilms = res?.results || [];

          setPopularFilms(prev => {
            const combined = [...prev, ...newFilms];
            const unique = combined.filter(
              (film, index, self) => index === self.findIndex(f => f.id === film.id)
            );
            return unique;
          });

          console.log("res:", res);
        } catch (err) {
          console.error("Erreur API: ", err);
        }
      };
      fetchPopularMovies();
    }, 400);

    return () => clearTimeout(debounce);
  }, [pageNum]);


  const getColorFromNote = (note) => {
    const clampedNote = Math.max(0, Math.min(parseInt(note), 10)); 
    const hue = (clampedNote / 10) * 120;
    return `hsl(${hue}, 100%, 30%)`;
  }

  
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const winH = window.innerHeight;
      const docHeight = document.documentElement.scrollHeight;
  
      if (scrollTop + winH >= docHeight - 50 && !isFetching) {
        setIsFetching(true);
        setPageNum(prev => prev + 1);
        console.log("Bas de page");
      }
    };
    window.addEventListener("scroll", handleScroll);
    const checkInitialScroll = () => {
    const winH = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    if (winH >= docHeight && !isFetching) {
      setIsFetching(true);
      setPageNum(prev => prev + 1);
      console.log("Contenu trop court, chargement forcé");
    }
  };

  checkInitialScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, [isFetching]);

  useEffect(() => {
    if (isFetching) {
      const timer = setTimeout(() => {
        setIsFetching(false);
      }, 2000); // à adapter selon la durée de ton fetch
      return () => clearTimeout(timer);
    }
  }, [isFetching]);

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
                  <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
                    <h3>{film.title}</h3>
                    <span>⭐{film.vote_count}</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
                    <p>{film.release_date.slice(0, 4)}</p>
                    <p><span style={{ color: getColorFromNote(film.vote_average)}}>{film.vote_average.toString().slice(0,3)}</span>/10</p>
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

