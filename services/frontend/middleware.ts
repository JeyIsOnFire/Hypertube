import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import jwt from 'jsonwebtoken';

const SUPPORTED_LOCALES = ['fr', 'en'];
const DEFAULT_LOCALE = 'fr';
const tmp_env = "django-insecure-)gihwu0k6z0aisy31^z#_9go(2fg))2e)(quptz!$lf*1pk+!5";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('access_token')?.value;
  let isTokenValid = false;

  const currentLocale = SUPPORTED_LOCALES.find((locale) =>
    pathname.startsWith(`/${locale}`)
  );

  const locale =
    currentLocale ||
    request.cookies.get('NEXT_LOCALE')?.value ||
    request.headers.get('accept-language')?.split(',')[0].split('-')[0] ||
    DEFAULT_LOCALE;

  // Redirect if locale is missing
  if (!currentLocale) {
    const url = request.nextUrl.clone();
    url.pathname = `/${locale}${pathname}`;
    const response = NextResponse.redirect(url);
    response.cookies.set('NEXT_LOCALE', locale, { path: '/' });
    return response;
  }

  // Validate token
  if (token) {
    try {
      jwt.verify(token, tmp_env);
      isTokenValid = true;
    } catch {
      request.cookies.set('access_token', '', { path: '/', maxAge: 0 });
    }
  }

  const authPath = pathname.startsWith(`/${locale}/auth`);

  if (authPath && isTokenValid)
    return NextResponse.redirect(new URL(`/${locale}/`, request.url));

  if (!authPath && !isTokenValid) {
    return NextResponse.redirect(
      new URL(`/${locale}/auth/login`, request.url)
    );
  }

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
