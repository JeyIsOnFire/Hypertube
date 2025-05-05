import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PUBLIC_FILE = /\.(.*)$/;
const SUPPORTED_LOCALES = ['fr', 'en'];
const DEFAULT_LOCALE = 'fr';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Ignorer les fichiers statiques et l'API
  if (PUBLIC_FILE.test(pathname) || pathname.startsWith('/api')) {
    return NextResponse.next();
  }

  // Vérifier si la langue est déjà présente dans l'URL (/fr, /en)
  const pathnameIsMissingLocale = SUPPORTED_LOCALES.every(
    (locale) => !pathname.startsWith(`/${locale}`)
  );

  // Si la langue est absente dans l'URL, on effectue la redirection
  if (pathnameIsMissingLocale) {
    // 1. Vérifier si un cookie est déjà défini
    const cookieLocale = request.cookies.get('NEXT_LOCALE')?.value;

    // 2. Utiliser la langue du navigateur (accept-language)
    const acceptLang = request.headers.get('accept-language');
    const preferredLang = acceptLang?.split(',')[0].split('-')[0];

    // Déterminer la langue à utiliser
    const locale =
      cookieLocale && SUPPORTED_LOCALES.includes(cookieLocale)
        ? cookieLocale
        : preferredLang && SUPPORTED_LOCALES.includes(preferredLang)
        ? preferredLang
        : DEFAULT_LOCALE;

    const url = request.nextUrl.clone();
    url.pathname = `/${locale}${pathname === '/' ? '' : pathname}`;

    const response = NextResponse.redirect(url);
    response.cookies.set('NEXT_LOCALE', locale, { path: '/' });

    return response;
  }

  // Si la langue est déjà présente et correcte, passer au suivant
  return NextResponse.next();
}

function setLocale(request: NextRequest) {
}
