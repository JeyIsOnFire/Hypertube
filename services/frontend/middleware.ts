import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import jwt from 'jsonwebtoken';

const PUBLIC_FILE = /\.(.*)$/;
const SUPPORTED_LOCALES = ['fr', 'en'];
const DEFAULT_LOCALE = 'fr';
let LOCAL: string;
const tmp_env = "django-insecure-)gihwu0k6z0aisy31^z#_9go(2fg))2e)(quptz!$lf*1pk+!5"

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('access_token')?.value;
  let isTokenValid: boolean = false;

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
    LOCAL =
      cookieLocale && SUPPORTED_LOCALES.includes(cookieLocale)
        ? cookieLocale
        : preferredLang && SUPPORTED_LOCALES.includes(preferredLang)
        ? preferredLang
        : DEFAULT_LOCALE;

    const url = request.nextUrl.clone();
    url.pathname = `/${LOCAL}${pathname === '/' ? '' : pathname}`;

    const response = NextResponse.redirect(url);
    response.cookies.set('NEXT_LOCALE', LOCAL, { path: '/' });

    return response;
  }

  //If there is no access token, redirection to login page
  if (!token)
    return NextResponse.redirect(new URL(`${LOCAL}/auth/login`, request.url));

  //If there is an access token, check the validity
  try {
      jwt.verify(token, tmp_env);
      isTokenValid = true;
  } catch {
    request.cookies.remove('access_token');
  }

  if (pathname.startsWith(`${LOCAL}/auth/`) && isTokenValid)
      return NextResponse.redirect(new URL('/', request.url));

  if (!pathname.startsWith(`${LOCAL}/auth/`) && !isTokenValid)
      return NextResponse.redirect(new URL(`${LOCAL}/auth/login`, request.url));

  // Si la langue est déjà présente et correcte, passer au suivant
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all routes except:
     * - API routes (/api/**)
     * - Static files (/static/**, /_next/**, /favicon.ico, etc.)
    */
    '/((?!api|_next/static|_next/image|favicon.ico|static).*)',
  ],
};
