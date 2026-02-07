import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect routes
export function middleware(request: NextRequest) {
  // Paths that don't require authentication
  const publicPaths = ['/login', '/signup'];

  // Protected paths that should be handled client-side
  const clientProtectedPaths = ['/dashboard', '/tasks', '/']; // Add other protected pages here - '/' is the home page

  // Check if current path is a public path
  const isPublicPath = publicPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // Check if current path is client-protected (handled client-side)
  const isClientProtectedPath = clientProtectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // Check if the user has a token by looking for Authorization header or by attempting to validate the token
  // This works when the client sends requests with the Bearer token
  const hasAuthHeader = request.headers.get('authorization')?.startsWith('Bearer ');

  // For protected paths that are NOT client-protected, if there's no auth header, redirect to login
  if (!isPublicPath && !isClientProtectedPath && !hasAuthHeader) {
    // Check if it's an API call (starts with /api or /auth)
    if (request.nextUrl.pathname.startsWith('/api') || request.nextUrl.pathname.startsWith('/auth')) {
      // For API calls without auth, let them pass through to the backend to handle the 401
      return NextResponse.next();
    } else {
      // For page requests without auth, redirect to login
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  // For client-protected paths, we need to handle authentication differently
  // Since these pages will do client-side auth checks, we can allow them to proceed
  // But for the root path specifically, we can add an extra check to improve UX
  if (isClientProtectedPath) {
    // For initial visits to protected pages, we can check for the existence of a token in cookies or headers
    // However, since the frontend stores tokens in localStorage, we can't check that server-side
    // So we'll let the client-side handle it, but we can add a small optimization
    return NextResponse.next();
  }

  return NextResponse.next();

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