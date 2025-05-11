(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push(["chunks/[root-of-the-server]__de110ef0._.js", {

"[externals]/node:buffer [external] (node:buffer, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("node:buffer", () => require("node:buffer"));

module.exports = mod;
}}),
"[externals]/node:async_hooks [external] (node:async_hooks, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("node:async_hooks", () => require("node:async_hooks"));

module.exports = mod;
}}),
"[project]/middleware.ts [middleware-edge] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.s({
    "middleware": (()=>middleware)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$esm$2f$api$2f$server$2e$js__$5b$middleware$2d$edge$5d$__$28$ecmascript$29$__$3c$module__evaluation$3e$__ = __turbopack_context__.i("[project]/node_modules/next/dist/esm/api/server.js [middleware-edge] (ecmascript) <module evaluation>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$web$2f$spec$2d$extension$2f$response$2e$js__$5b$middleware$2d$edge$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/esm/server/web/spec-extension/response.js [middleware-edge] (ecmascript)");
;
const PUBLIC_FILE = /\.(.*)$/;
const SUPPORTED_LOCALES = [
    'fr',
    'en'
];
const DEFAULT_LOCALE = 'fr';
function middleware(request) {
    const { pathname } = request.nextUrl;
    // Ignorer les fichiers statiques et l'API
    if (PUBLIC_FILE.test(pathname) || pathname.startsWith('/api')) {
        return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$web$2f$spec$2d$extension$2f$response$2e$js__$5b$middleware$2d$edge$5d$__$28$ecmascript$29$__["NextResponse"].next();
    }
    // Vérifier si la langue est déjà présente dans l'URL (/fr, /en)
    const pathnameIsMissingLocale = SUPPORTED_LOCALES.every((locale)=>!pathname.startsWith(`/${locale}`));
    // Si la langue est absente dans l'URL, on effectue la redirection
    if (pathnameIsMissingLocale) {
        // 1. Vérifier si un cookie est déjà défini
        const cookieLocale = request.cookies.get('NEXT_LOCALE')?.value;
        // 2. Utiliser la langue du navigateur (accept-language)
        const acceptLang = request.headers.get('accept-language');
        const preferredLang = acceptLang?.split(',')[0].split('-')[0];
        // Déterminer la langue à utiliser
        const locale = cookieLocale && SUPPORTED_LOCALES.includes(cookieLocale) ? cookieLocale : preferredLang && SUPPORTED_LOCALES.includes(preferredLang) ? preferredLang : DEFAULT_LOCALE;
        const url = request.nextUrl.clone();
        url.pathname = `/${locale}${pathname === '/' ? '' : pathname}`;
        const response = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$web$2f$spec$2d$extension$2f$response$2e$js__$5b$middleware$2d$edge$5d$__$28$ecmascript$29$__["NextResponse"].redirect(url);
        response.cookies.set('NEXT_LOCALE', locale, {
            path: '/'
        });
        return response;
    }
    // Si la langue est déjà présente et correcte, passer au suivant
    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$web$2f$spec$2d$extension$2f$response$2e$js__$5b$middleware$2d$edge$5d$__$28$ecmascript$29$__["NextResponse"].next();
}
function setLocale(request) {}
}}),
}]);

//# sourceMappingURL=%5Broot-of-the-server%5D__de110ef0._.js.map