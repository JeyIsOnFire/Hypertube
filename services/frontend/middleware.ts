import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

const SUPPORTED_LOCALES = ['fr', 'en'];
const DEFAULT_LOCALE = 'fr';
const JWT_KEY = process.env.JWT_KEY;

export async function middleware(request: NextRequest) {
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
    const payload = await verifyToken(token);
    if (payload)
      isTokenValid = true;
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

async function verifyToken(token: string) {
  try {
    const secretKey = new TextEncoder().encode(JWT_KEY);
    const { payload } = await jwtVerify(token, secretKey);
    return payload;
  } catch (err) {
    console.error("JWT verification failed:", err.message);
    return null;
  }
}

export const config = {
  matcher: [
    /*
     * Match all routes except:
     * - API routes (/api/**)
     * - Static files (/static/**, /_next/**, /favicon.ico, etc.)
    */
    '/((?!api|_next|static|favicon.ico|__nextjs|robots.txt|sitemap.xml).*)',
  ],
};
