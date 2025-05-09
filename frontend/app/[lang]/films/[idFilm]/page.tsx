"use client";

import React, { useState, useEffect, use } from "react";
import { fetchApi } from "@/lib/fetch-api";
import styles from "./filmPage.module.css";

interface MovieData {
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
}

export default function FilmPage({ params, }: { params: Promise<{ idFilm: string }>; }) {

  const { idFilm } = use(params);
  const [movieData, setMovieData] = useState<MovieData | null>(null);

  useEffect(() => {
    const fetchMovieData = async () => {
      try {
        const res = await fetchApi(`getMovieInfosById/${idFilm}`);
        setMovieData(res);
      } catch (err) {
        console.error("Erreur API: ", err);
      }
    };
    fetchMovieData();
  }, [idFilm]);

  if (!movieData) {
    return <div>Chargement...</div>;
  }

  console.log("movieData:", movieData);
  // const { adult, backdrop_path, belongs_to_collection, budget, genres, homepage, id, imdb_id, origin_country, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count } = movieData;

  return (
    <div className={styles.pageContainer}>
      {/* Arrière-plan flou */}
      <div
        className={styles.background}
        style={{
          backgroundImage: `url(https://image.tmdb.org/t/p/w300${movieData.backdrop_path ? movieData.backdrop_path : movieData.poster_path})`,
        }}
      ></div>

      {/* Contenu principal */}
      <main className={styles.content}>
        <h2>{movieData.original_title}</h2>
        <img
          src={`https://image.tmdb.org/t/p/w300${movieData.poster_path}`}
          alt={`Affiche de ${movieData.original_title}`}
          className={styles.poster}
        />
        <p className={styles.overview}>{movieData.overview}</p>
        <ul className={styles.details}>
          <li>
            <strong>Genre :</strong> {movieData.genres[0]?.name || "N/A"}
          </li>
          <li>
            <strong>Durée :</strong> {movieData.runtime} min
          </li>
          <li>
            <strong>Année :</strong> {movieData.release_date.split("-")[0]}
          </li>
        </ul>
        <button className={styles.watchButton}>Regarder maintenant</button>
        <div className={styles.videoContainer}>video</div>
      </main>
    </div>
  );
}
