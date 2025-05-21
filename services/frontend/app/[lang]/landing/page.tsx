"use client";

import React, { useState, useEffect, useRef, useCallback } from 'react';
import styles from './landing.module.css';
import Link from 'next/link';
import Image from 'next/image';
import { fetchApi } from '@/lib/fetch-api';
import translations from '@/locales';
import { usePathname } from 'next/navigation';

type Film = {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
  vote_average: number;
  vote_count: number;
}

type HeaderProps = {
  lang: 'fr' | 'en';
}

const Landing = ({ lang }: HeaderProps) => {

  const [popularFilms, setPopularFilms] = useState<Film[]>([]);
  const [pageNum, setPageNum] = useState<number>(1);
  const t = translations[lang];
  const isFetching = useRef(false);

  const checkIfBottom = useCallback(() => {
    const scrollTop = window.scrollY;
    const winH = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    return scrollTop + winH >= docHeight - 1;
  }, []);

  const tryLoadNextPage = useCallback(() => {
    if (!isFetching.current && checkIfBottom()) {
      isFetching.current = true;
      setPageNum(prev => prev + 1);
      console.log("Chargement page suivante");
    }
  }, [checkIfBottom, setPageNum, isFetching]);

  // Vérifie au scroll
  useEffect(() => {
    const handleScroll = () => tryLoadNextPage();
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [tryLoadNextPage]);

  // Vérifie aussi après chaque ajout de contenu
  useEffect(() => {
    const timeout = setTimeout(() => {
      isFetching.current = false;
      tryLoadNextPage(); // 👈 Si on est toujours en bas => on recharge
    }, 500); // Temps fictif de "chargement"

    return () => clearTimeout(timeout);
  }, [pageNum, tryLoadNextPage]);

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
  }, [pageNum, lang]);

  const pathname = usePathname();
  if (!pathname)  return null;


  const getColorFromNote = (note: number) => {
    const clampedNote = Math.max(0, Math.min(note, 10)); 
    const hue = (clampedNote / 10) * 120;
    return `hsl(${hue}, 100%, 30%)`;
  }

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
              key={index}
              href={`/films/${film['id']}`}
            >
              <div className={styles.info}>
                <Image src={`https://image.tmdb.org/t/p/w300${film.poster_path}`} alt={film.title} width={1080} height={1920}/>
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
