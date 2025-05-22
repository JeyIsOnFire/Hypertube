"use client";

import React, { useState, useEffect, use, useRef, useCallback } from 'react';
import styles from '../../landing/landing.module.css';
import Link from 'next/link';
import Image from 'next/image';
import { fetchApi } from '@/lib/fetch-api';
// import translations from '@/locales';
import { usePathname } from 'next/navigation';

type Film = {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
  vote_average: number;
  vote_count: number;
}

const SearchResultsPage = ({ params }: { params: Promise<{ lang: string; query: string }> }) => {

  const { lang, query } = use(params);
  const [searchedFilms, setSearchedFilms] = useState<Film[]>([]);
  const [popularFilms, setPopularFilms] = useState<Film[]>([]);
  // const t = translations[lang as keyof typeof translations];

  useEffect(() => {
    const debounce = setTimeout(() => {
      const fetchSearchedMovies = async () => {
        try {
          const res = await fetchApi(`${lang}/fetchMovieData?query=${encodeURIComponent(query)}`);
          const newFilms = res?.results || [];
          if (newFilms.length === 0) {
            const popularRes = await fetchApi(`${lang}/fetchPopularMovies/1`);
            setPopularFilms(popularRes?.results || []);
          } else {
            setSearchedFilms(prev => {
              const combined = [...prev, ...newFilms];
              const unique = combined.filter(
                (film, index, self) => index === self.findIndex(f => f.id === film.id)
              );
              return unique;
            });
          }
        } catch (err) {
          console.error("Erreur API: ", err);
        }
      };
      fetchSearchedMovies();
    }, 400);

    return () => clearTimeout(debounce);
  }, [lang]);

  const pathname = usePathname();
  if (!pathname)  return null;


  const getColorFromNote = (note: number) => {
    const clampedNote = Math.max(0, Math.min(note, 10)); 
    const hue = (clampedNote / 10) * 120;
    return `hsl(${hue}, 100%, 30%)`;
  }

  return (
    <>
      {/*----------------------------- RESULTS SEARCH -----------------------------*/}
      <section className={styles.grid}>
        {!popularFilms.length && !searchedFilms.length && (
          <div style={{ height: '100vh'}}>
          </div>
        )}
        {(searchedFilms.length !== 0 ? [...searchedFilms] : [...popularFilms])
          .sort((a, b) => a.title.localeCompare(b.title)).map((film, index: number) => (
          <div key={film.id} className={styles.card}>
            <Link
              key={index}
              href={`/films/${film['id']}`}
            >
              <div className={styles.info}>
              <Image
                src={film.poster_path ? `https://image.tmdb.org/t/p/w300${film.poster_path}` : '/fallback.png'}
                alt={film.title}
                width={1080}
                height={1920}
                onError={(e) => { (e.target as HTMLImageElement).src='/fallback.png'; }}
              />
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

export default SearchResultsPage;
