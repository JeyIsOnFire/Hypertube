// lib/getTranslations.ts
import fr from '@/locales/fr';
import en from '@/locales/en';

const translations: Record<string, any> = {
  fr,
  en,
};

function getTranslations(lang: string) {
  return translations[lang] || translations['en'];
}

export default getTranslations;
