'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useParams } from 'next/navigation';

const SUPPORTED_LOCALES = ['fr', 'en'];

export default function LanguageSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const params = useParams();

  const currentLang = params.lang;
  const otherLang = SUPPORTED_LOCALES.find(l => l !== currentLang);

  const switchLang = () => {
    const segments = pathname.split('/');
    segments[1] = otherLang!; // remplace le segment langue
    const newPath = segments.join('/');
    router.push(newPath);

    // (optionnel) mettre à jour le cookie
    document.cookie = `NEXT_LOCALE=${otherLang}; path=/`;
  };

  const flags = {
    fr: (
      <svg viewBox="0 -4 28 28" width="24" height="16" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="28" height="20" fill="white" />
        <rect x="0" y="0" width="9.33" height="20" fill="#1035BB" />
        <rect x="18.66" y="0" width="9.33" height="20" fill="#F44653" />
      </svg>
    ),
    en: (
      <svg viewBox="0 -4 28 28" width="24" height="16" xmlns="http://www.w3.org/2000/svg">
        <rect width="28" height="20" rx="2" fill="white" />
        <path d="M0,2h28M0,6h28M0,10h28M0,14h28M0,18h28" stroke="#D02F44" strokeWidth="2" />
        <rect width="12" height="9" fill="#46467F" />
      </svg>
    )
  };


  return (
	<>
	  <button style={{position: 'absolute', cursor: 'pointer', zIndex: '3'}} onClick={switchLang}>
		{flags[otherLang]}
	  </button>
	</>
  );
}

