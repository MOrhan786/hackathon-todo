'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth-service';

export default function DashboardPage() {
  const router = useRouter();
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    // Check authentication status on the client side
    if (typeof window !== 'undefined') {
      // Small delay to ensure token is properly stored after redirect
      const timer = setTimeout(() => {
        const authenticated = authService.isAuthenticated();

        if (!authenticated) {
          router.replace('/login'); // Redirect to login if not authenticated
        } else {
          // If authenticated, redirect to the main todo app page
          router.replace('/');
        }
      }, 100); // Small delay to ensure token is available

      return () => clearTimeout(timer);
    }
  }, [router]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold">Redirecting...</h1>
      <p className="mt-2 text-gray-500">Loading your todo app...</p>
    </div>
  );
}
