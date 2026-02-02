'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth-service';

export default function DashboardPage() {
  const router = useRouter();
  useEffect(() => {
    // Check authentication status on the client side
    if (typeof window !== 'undefined') {
      const authenticated = authService.isAuthenticated();

      if (!authenticated) {
        router.replace('/login'); // Redirect to login if not authenticated
      } else {
        // If authenticated, redirect to the main todo app page
        router.replace('/');
      }
    }
  }, [router]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold">Redirecting...</h1>
      <p className="mt-2 text-gray-500">Loading your todo app...</p>
    </div>
  );
}
