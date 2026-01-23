import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect routes
export function middleware(request: NextRequest) {
  // Paths that don't require authentication
  const publicPaths = ['/login', '/signup'];

  // Check if current path is a public path
  const isPublicPath = publicPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // Check if the user has a token in localStorage by looking for Authorization header in API calls
  // This works when the client sends requests with the Bearer token
  const hasAuthHeader = request.headers.get('authorization')?.startsWith('Bearer ');

  // For protected paths, if there's no auth header, redirect to login
  if (!isPublicPath && !hasAuthHeader) {
    // Check if it's an API call (starts with /api or /auth)
    if (request.nextUrl.pathname.startsWith('/api') || request.nextUrl.pathname.startsWith('/auth')) {
      // For API calls without auth, let them pass through to the backend to handle the 401
      return NextResponse.next();
    } else {
      // For page requests without auth, redirect to login
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

// Specify which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - auth (auth routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - sitemap.xml (sitemap file)
     * - robots.txt (robots file)
     */
    '/((?!api|auth|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
  ],
}