"use client";

import React, { useState, useEffect, use } from "react";
import { fetchApi } from "@/lib/fetch-api";
import styles from "./filmPage.module.css";
import translations from "@/locales";
import Image from "next/image";
import { usePathname } from "next/navigation";

interface MovieData {
  movie_data: {
    adult: boolean;
    backdrop_path: string;
    belongs_to_collection: null | string;
    budget: number;
    genres: Array<{ id: number; name: string }>;
    homepage: string;
    id: number;
    imdb_id: string;
    origin_country: Array<string>;
    original_language: string;
    original_title: string;
    overview: string;
    popularity: number;
    poster_path: string;
    production_companies: Array<{ id: number; logo_path: null | string; name: string; origin_country: string }>;
    production_countries: Array<{ iso_3166_1: string; name: string }>;
    release_date: string;
    revenue: number;
    runtime: number;
    spoken_languages: Array<{ english_name: string; iso_639_1: string; name: string }>;
    status: string;
    tagline: null | string;
    title: string;
    video: boolean;
    vote_average: number;
    vote_count: number;
  },
  credits_data: {
    cast: Array<{ id: number; name: string; character: string; profile_path: null | string }>;
    crew: Array<{ id: number; name: string; job: string; profile_path: null | string }>;
  };
}


export default function FilmPage({ params }: { params: Promise<{ idFilm: string }>; }) {

  const { idFilm } = use(params);
  const [movieData, setMovieData] = useState<MovieData | null>(null);
  let lang = "en";
  // const lang = use(params).lang;
  //
  useEffect(() => {

    const fetchMovieData = async () => {
      try {
        const res = await fetchApi(`${lang}/getMovieInfosById/${idFilm}`);
        setMovieData(res);
      } catch (err) {
        console.error("Erreur API: ", err);
      }
    };
    fetchMovieData();
  }, [idFilm, lang]);

  const pathname = usePathname();
  if (!pathname) return null;
  lang = pathname.split('/')[1] as 'fr' | 'en';

  if (!movieData) {
    return <div style={{height: '100vh'}}></div>;
  }

  const t = translations[lang as 'fr' | 'en'];
  if (!t) {
    console.error(`Missing translations for lang: ${lang}`);
    return null;
  }

  console.log("movieData:", movieData);
  // const { adult, backdrop_path, belongs_to_collection, budget, genres, homepage, id, imdb_id, origin_country, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count } = movieData;

  return (
    <div className={styles.pageContainer}>
      {/* Arrière-plan flou */}
      <div
        className={styles.background}
        style={{
          backgroundImage: `url(https://image.tmdb.org/t/p/w300${movieData["movie_data"].backdrop_path ? movieData["movie_data"].backdrop_path : movieData["movie_data"].poster_path})`,
        }}
      ></div>

      {/* Contenu principal */}
      <main className={styles.content}>
        <h2>{movieData["movie_data"].original_title}</h2>
        <div className={styles.row}>
          <Image
            src={`https://image.tmdb.org/t/p/w300${movieData["movie_data"].poster_path}`}
            alt={`Affiche de ${movieData["movie_data"].original_title}`}
            className={styles.poster}
            width={200}
            height={400}
          />
          <ul className={styles.details}>
            <li>
              <strong>{t.genre} :</strong> {movieData["movie_data"].genres?.map((genre) => genre.name).join(", ") || "N/A"}
            </li>
            <li>
              <strong>{t.duration} :</strong> {movieData["movie_data"].runtime} min
            </li>
            <li>
              <strong>{t.year} :</strong> {movieData["movie_data"].release_date.split("-")[0]}
            </li>
            <li>
              <strong>{t.rating} :</strong> {movieData["movie_data"].vote_average} / 10
            </li>
            <li>
              <strong>{t.voteCount} :</strong> {movieData["movie_data"].vote_count} votes
            </li>
            <li>
              <strong>{t.casting} :</strong> {movieData["credits_data"]["cast"].slice(0, 3).map((actor) => actor.name).join(", ") || "N/A"}
            </li>
            <li>
              <strong>{t.production} :</strong> {movieData["credits_data"]["crew"].slice(0, 3).map((worker) =>worker.name).join(", ") || "N/A"}
            </li>
          </ul>
        </div>

        <p className={styles.overview}>{movieData["movie_data"].overview}</p>
        <button className={styles.watchButton}>{t.watchnow}</button>
        <div className={styles.videoContainer}>video</div>
      </main>
    </div>
  );
}
