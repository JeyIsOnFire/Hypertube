"use client";

import React, { useState, useEffect, useRef } from 'react';
import styles from './header.module.css';
import LanguageSwitcher from '../components/language-switcher';
import translations from '@/locales';
import {fetchApi, logout} from '@/lib/fetch-api';
import Link from 'next/link';
import Burger from '../components/burger';
import { Monoton } from 'next/font/google';
import { useRouter } from 'next/navigation';

const monoton = Monoton({ subsets: ['latin'], weight: '400' });


type HeaderProps = {
  lang: 'fr' | 'en';
};

const Header = ({ lang }: HeaderProps) => {

  const router = useRouter();
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState(null); 

  const resultRef = useRef<HTMLDivElement>(null);
  const boutonRef = useRef<HTMLButtonElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const t = translations[lang];
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 600);
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (resultRef.current) {
        console.log('contains', resultRef.current.contains(event.target as Node));
      }
      if (event.target !== boutonRef.current && event.target !== inputRef.current && resultRef.current && !resultRef.current.contains(event.target as Node)) {
        console.log('clicked outside');
        setIsSearching(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => { document.removeEventListener('mousedown', handleClickOutside); }
  }, []);

  useEffect(() => {
    if (query === '') return;

    const debounce = setTimeout(() => {
      const fetchData = async () => {
        try {
          const res = await fetchApi(`${lang}/fetchMovieData?query=${encodeURIComponent(query)}`);
          setResponse(res);
        } catch (err) {
          console.error("Erreur API :", err);
        }
      };
      fetchData();
    }, 1000);

    return () => clearTimeout(debounce);
  }, [query, lang]);

  const toggleSearch = () => {
    setIsSearching(!isSearching);
  }
  const handleSearch = (e: React.MouseEvent<HTMLButtonElement> | React.KeyboardEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (query !== '') {
      router.push(`/searchResults/${query}`);
      setIsSearching(false);
    }
  }

  return (
    <>
      <header className={styles.header}>
      {/*----------------------------- BURGER -----------------------------*/}
      {isMobile ? (
        <>
          <div className={styles.headerContainer}>
            <div className={styles.row}>
              <Link href="#"><svg onClick={toggleSearch} className={styles.searchIcon} xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px">
                <path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/>
              </svg></Link>
              <Link href="#"><svg className={styles.logoutIcon} width="30px" height="30px" viewBox="0 0 512 512" onClick={logout}>
                <path d="m400 54.1c63 45 104 118.6 104 201.9 0 136.8-110.8 247.7-247.5 248-136.5.3-248.3-111-248.5-247.6-.1-83.3 40.9-157.1 103.8-202.2 11.7-8.3 28-4.8 35 7.7l15.8 28.1c5.9 10.5 3.1 23.8-6.6 31-41.5 30.8-68 79.6-68 134.9-.1 92.3 74.5 168.1 168 168.1 91.6 0 168.6-74.2 168-169.1-.3-51.8-24.7-101.8-68.1-134-9.7-7.2-12.4-20.5-6.5-30.9l15.8-28.1c7-12.4 23.2-16.1 34.8-7.8zm-104 209.9v-240c0-13.3-10.7-24-24-24h-32c-13.3 0-24 10.7-24 24v240c0 13.3 10.7 24 24 24h32c13.3 0 24-10.7 24-24z" />
              </svg></Link>
            </div>
            <div className={styles.top}>
              <h1><Link href="/">HYPERTUBE</Link></h1>
            </div>
            <div className={styles.burger}>
              <Burger lang={lang}/>
            </div>
          </div>
        </>
      ) : (
        <>
          <LanguageSwitcher />
          <div className={`${monoton.className} ${styles.top}`}>
            <h1><Link href="/">HYPERTUBE</Link></h1>
          </div>

          <nav className={styles.nav}>
            <Link href="/">{t.home}</Link>
            <a href="#">{t.movies}</a>
            <a href="#">{t.shows}</a>
            <Link href="/account/">{t.myaccount}</Link>
            <a><svg onClick={toggleSearch} className={styles.searchIcon} xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px">
              <path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/>
            </svg></a>
            <a onClick={logout}><svg className={styles.logoutIcon} width="30px" height="30px" viewBox="0 0 512 512" >
              <path d="m400 54.1c63 45 104 118.6 104 201.9 0 136.8-110.8 247.7-247.5 248-136.5.3-248.3-111-248.5-247.6-.1-83.3 40.9-157.1 103.8-202.2 11.7-8.3 28-4.8 35 7.7l15.8 28.1c5.9 10.5 3.1 23.8-6.6 31-41.5 30.8-68 79.6-68 134.9-.1 92.3 74.5 168.1 168 168.1 91.6 0 168.6-74.2 168-169.1-.3-51.8-24.7-101.8-68.1-134-9.7-7.2-12.4-20.5-6.5-30.9l15.8-28.1c7-12.4 23.2-16.1 34.8-7.8zm-104 209.9v-240c0-13.3-10.7-24-24-24h-32c-13.3 0-24 10.7-24 24v240c0 13.3 10.7 24 24 24h32c13.3 0 24-10.7 24-24z" />
            </svg></a>
          </nav>
        </>
      )}
      </header>

      {/*----------------------------- SEARCH BAR -----------------------------*/}
      <div className={`overflow-hidden ${isSearching ? styles.searchBarOpened : 'max-h-0'}`}>
        <svg  className={styles.searchIcon2} xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 50 50" width="50px" height="50px">
          <path d="M 21 3 C 11.601563 3 4 10.601563 4 20 C 4 29.398438 11.601563 37 21 37 C 24.355469 37 27.460938 36.015625 30.09375 34.34375 L 42.375 46.625 L 46.625 42.375 L 34.5 30.28125 C 36.679688 27.421875 38 23.878906 38 20 C 38 10.601563 30.398438 3 21 3 Z M 21 7 C 28.199219 7 34 12.800781 34 20 C 34 27.199219 28.199219 33 21 33 C 13.800781 33 8 27.199219 8 20 C 8 12.800781 13.800781 7 21 7 Z"/>
        </svg>
        <div className={styles.searchInputContainer}>
          <input 
            onChange={(e) => setQuery(e.target.value)} 
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSearch(e);
              }
            }}
            className={styles.searchInput}
            type="text"
            placeholder={t.search}
            ref={inputRef}>
          </input>
          <button 
            ref={boutonRef}
            onClick={handleSearch}
            // href={`/searchResults/${query}`}
            className={styles.searchButton}>{t.searchButton}
          </button>
        </div>
      </div>

      {/*----------------------------- SEARCH RESULTS -----------------------------*/}
      {response && isSearching && (() => {

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
        if (Array.isArray(parsed) && parsed.length > 0) {
          return (
            <div className={styles.results} ref={resultRef}>
              <div className={styles.filmList}>
                {parsed.slice(0, 10).map((film, index: number) => (
                  <Link
                    onClick={()=> { setResponse(null); setIsSearching(false) }}
                    key={index}
                    href={`/films/${film['id']}`}
                    className={styles.filmCard}
                  >
                    <h3>{film['title']}</h3>
                    <p>{film['release_date'].slice(0, 4)}</p>
                  </Link>
                ))}
              </div>
            </div>
          );
        } else {
          return (
            <div className={styles.results} ref={resultRef}>
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
