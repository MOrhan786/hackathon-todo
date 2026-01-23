'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth-service';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallbackUrl?: string; // Where to redirect if not authenticated (default: /login)
}

export default function ProtectedRoute({ children, fallbackUrl = '/login' }: ProtectedRouteProps) {
  const router = useRouter();

  useEffect(() => {
    // Check authentication status on mount
    if (!authService.isAuthenticated()) {
      router.push(fallbackUrl);
    }
  }, [router, fallbackUrl]);

  // If not authenticated, don't render children (redirect will happen)
  if (!authService.isAuthenticated()) {
    return null;
  }

  return <>{children}</>;
}