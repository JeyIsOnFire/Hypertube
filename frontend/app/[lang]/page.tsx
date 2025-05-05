"use client";

import React from 'react';
import { useEffect, useState } from 'react';
import { fetchApi } from './components/fetch-api';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';


interface Poster {
  tconst: string;
  title: string;
  poster_url: string;
}

const Home = () => {
  const router = useRouter();
  const [posters, setPosters] = useState<Poster[]>([]);

  useEffect(() => {
    fetchApi("randomPoster")
      .then((response: Poster[]) => {
        console.log("API Response:", response); // Affiche la réponse dans la console
        setPosters(response);
      })
      .catch((error: Error) => console.error("API Error:", error));
  }, []);

  const goToLanding = () => {
	router.push('landing');
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="text-4xl font-bold mb-4">Random Posters</h1>

	  <Link href="landing" className="bg-red-600 pointer p-1 mb-3">
	    Idee de design:
	    <button className="cursor-pointer">CLIQUEZ ICI</button>
	  </Link>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {posters.lenght > 0 ? (
          posters.map((poster, index) => (
            <div key={poster.tconst || index} className="bg-gray-200 p-4 rounded-lg shadow-md">
              <img src={poster.poster_url} alt={poster.title} className="rounded-lg" />
              <p className="mt-2 text-center font-medium">{poster.title}</p>
            </div>
          ))
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
};

export default Home;
