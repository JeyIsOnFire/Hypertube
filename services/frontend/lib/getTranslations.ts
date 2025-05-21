// lib/getTranslations.ts


import translations from '@/locales';

function getTranslations(lang: string) {
  return translations[lang as 'en' | 'fr'] || translations['en'];
}

export default getTranslations;
