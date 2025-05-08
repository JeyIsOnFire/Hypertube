"use client";

import React, { useState, useEffect, useRef } from 'react';
import styles from './header.module.css';
import LanguageSwitcher from '../components/language-switcher';
import translations from '@/locales';
import { fetchApi } from '@/lib/fetch-api';
import Link from 'next/link';
import Burger from '../components/burger';

type HeaderProps = {
  lang: 'fr' | 'en';
};

const Header: React.FC<HeaderProps> = ({ lang }) => {

  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState(null); 
  const resultRef = useRef<HTMLDivElement>(null);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const t = translations[lang];
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 600);
    };

    // Vérifie la taille initiale de l'écran
    handleResize();

    // Ajoute un écouteur pour les redimensionnements
    window.addEventListener('resize', handleResize);

    // Nettoie l'écouteur lors du démontage du composant
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (resultRef.current && !resultRef.current.contains(event.target as Node)) {
        setResponse(null);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    }
  }, []);

  useEffect(() => {
    if (query === '') return;

    const debounce = setTimeout(() => {
      const fetchData = async () => {
        try {
          const res = await fetchApi(`fetchMovieData?query=${encodeURIComponent(query)}`);
          setResponse(res);
        } catch (err) {
          console.error("Erreur API :", err);
        }
      };
      fetchData();
    }, 1000);

    return () => clearTimeout(debounce);
  }, [query]);

  const toggleSearch = () => {
    setIsSearching(!isSearching);
  }

  return (
    <>
      <header className={styles.header}>
      {isMobile ? (
        <>
          <div className={styles.headerContainer}>
            <div className={styles.row}>
              <a><svg onClick={toggleSearch} className={styles.searchIcon} xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px">
                <path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/>
              </svg></a>
              <a><svg className={styles.logoutIcon} width="30px" height="30px" viewBox="0 0 512 512" >
                <path d="m400 54.1c63 45 104 118.6 104 201.9 0 136.8-110.8 247.7-247.5 248-136.5.3-248.3-111-248.5-247.6-.1-83.3 40.9-157.1 103.8-202.2 11.7-8.3 28-4.8 35 7.7l15.8 28.1c5.9 10.5 3.1 23.8-6.6 31-41.5 30.8-68 79.6-68 134.9-.1 92.3 74.5 168.1 168 168.1 91.6 0 168.6-74.2 168-169.1-.3-51.8-24.7-101.8-68.1-134-9.7-7.2-12.4-20.5-6.5-30.9l15.8-28.1c7-12.4 23.2-16.1 34.8-7.8zm-104 209.9v-240c0-13.3-10.7-24-24-24h-32c-13.3 0-24 10.7-24 24v240c0 13.3 10.7 24 24 24h32c13.3 0 24-10.7 24-24z" />
              </svg></a>
            </div>
            <div className={styles.top}>
              <h1>HYPERTUBE.LAJA</h1>
            </div>
            <div className={styles.burger}>
              <Burger />
            </div>
          </div>
        </>
      ) : (
        <>
          <LanguageSwitcher />
          <div className={styles.top}>
            <h1>HYPERTUBE.LAJA</h1>
          </div>

          <nav className={styles.nav}>
            <a href="#">{t.home}</a>
            <a href="#">{t.movies}</a>
            <a href="#">{t.shows}</a>
            <a href="#">{t.trending}</a>
            <a href="#">{t.myaccount}</a>
            <a><svg onClick={toggleSearch} className={styles.searchIcon} xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px">
              <path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/>
            </svg></a>
            <a><svg className={styles.logoutIcon} width="30px" height="30px" viewBox="0 0 512 512" >
              <path d="m400 54.1c63 45 104 118.6 104 201.9 0 136.8-110.8 247.7-247.5 248-136.5.3-248.3-111-248.5-247.6-.1-83.3 40.9-157.1 103.8-202.2 11.7-8.3 28-4.8 35 7.7l15.8 28.1c5.9 10.5 3.1 23.8-6.6 31-41.5 30.8-68 79.6-68 134.9-.1 92.3 74.5 168.1 168 168.1 91.6 0 168.6-74.2 168-169.1-.3-51.8-24.7-101.8-68.1-134-9.7-7.2-12.4-20.5-6.5-30.9l15.8-28.1c7-12.4 23.2-16.1 34.8-7.8zm-104 209.9v-240c0-13.3-10.7-24-24-24h-32c-13.3 0-24 10.7-24 24v240c0 13.3 10.7 24 24 24h32c13.3 0 24-10.7 24-24z" />
            </svg></a>
            <a><svg className={styles.settingsIcon} width="30px" height="30px"  x="0px" y="0px" viewBox="0 0 100 100">
              <path d="M97.779,60.931l-5.345-4.975c-1.39-1.294-2.214-3.115-2.271-5.011l-0.01-0.09l0.008-0.302   c0.048-1.986,0.936-3.881,2.436-5.201l5.495-4.808c0.863-0.757,1.161-1.98,0.737-3.047l-4.693-11.839   c-0.268-0.674-0.78-1.205-1.447-1.493c-0.378-0.163-0.763-0.235-1.178-0.219l-7.289,0.259c-1.051,0.039-2.122-0.164-3.098-0.586   c-0.871-0.376-1.634-0.901-2.278-1.565l-0.148-0.156c-1.312-1.428-1.99-3.36-1.864-5.301l0.485-7.287   c0.078-1.147-0.579-2.223-1.633-2.679L63.996,1.579c-1.053-0.455-2.285-0.197-3.067,0.643l-4.973,5.34   c-1.374,1.478-3.319,2.308-5.342,2.277c-0.939-0.015-1.854-0.212-2.719-0.586c-0.969-0.418-1.848-1.06-2.543-1.851l-4.81-5.496   c-0.268-0.305-0.592-0.543-0.965-0.703c-0.667-0.288-1.406-0.3-2.079-0.034L25.656,5.865c-1.066,0.422-1.754,1.476-1.713,2.623   l0.261,7.287c0.074,1.966-0.678,3.896-2.069,5.299l-0.096,0.097c-1.444,1.4-3.428,2.129-5.444,1.997l-7.29-0.484   c-1.143-0.077-2.218,0.58-2.674,1.634L1.579,36.006c-0.456,1.054-0.197,2.286,0.644,3.065l5.344,4.978   c1.414,1.316,2.241,3.177,2.274,5.18l-0.008,0.375c-0.089,1.936-0.977,3.775-2.431,5.045l-5.495,4.808   c-0.862,0.757-1.159,1.981-0.736,3.047l4.694,11.841c0.267,0.675,0.78,1.204,1.448,1.493c0.372,0.161,0.768,0.236,1.174,0.22   l7.29-0.261c1.048-0.04,2.121,0.166,3.097,0.588c0.858,0.37,1.606,0.884,2.34,1.629l0.189,0.206   c1.245,1.41,1.889,3.302,1.764,5.187l-0.487,7.289c-0.075,1.145,0.583,2.219,1.636,2.674l11.689,5.054   c1.053,0.455,2.285,0.197,3.065-0.641l4.949-5.314c1.34-1.439,3.234-2.279,5.263-2.305l0.142,0.004   c0.923,0.011,1.827,0.207,2.687,0.578c0.959,0.414,1.825,1.043,2.511,1.824l4.837,5.527c0.27,0.306,0.595,0.544,0.965,0.704   c0.665,0.288,1.404,0.299,2.08,0.032l11.842-4.695c1.066-0.421,1.755-1.475,1.713-2.619l-0.262-7.307   c-0.065-1.888,0.632-3.749,1.917-5.124l0.059-0.075l0.239-0.227c1.44-1.369,3.406-2.08,5.4-1.948l7.283,0.482   c1.144,0.076,2.22-0.579,2.676-1.634l5.052-11.688C98.877,62.944,98.619,61.712,97.779,60.931z M44.198,63.423   c-7.402-3.2-10.82-11.824-7.62-19.226c3.199-7.399,11.823-10.819,19.225-7.621c7.403,3.201,10.82,11.827,7.621,19.227   C60.224,63.206,51.6,66.624,44.198,63.423z" />
            </svg></a>
          </nav>
        </>
      )}
      </header>

      <div className={`overflow-hidden ${isSearching ? styles.searchBarOpened : 'max-h-0'}`}>
        <svg  className={styles.searchIcon2} xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px">
          <path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/>
        </svg>
        <input onChange={(e) => setQuery(e.target.value)} className={styles.searchInput} type="text" placeholder={t.search} />
      </div>

      {response && (() => {

       let parsed;
       if (typeof response === "string") {
         try {
           parsed = JSON.parse(response)['results'];
         } catch (error) {
           console.error("Failed to parse JSON:", error);
           return null;
         }
       } else if (typeof response === "object" && response !== null) {
         parsed = response['results'];
       } else {
         console.error("Unexpected response format:", response);
         return null;
   }
        console.log("JSON", parsed);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return (
            <div className={styles.results} ref={resultRef}>
              <div className={styles.filmList}>
                {parsed.slice(0, 10).map((film, index: number) => (
                  <Link
                    onClick={()=>setResponse(null)}
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

    </>
  )
}

export default Header;
