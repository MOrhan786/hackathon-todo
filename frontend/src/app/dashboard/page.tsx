'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import LoadingSpinner from '@/components/ui/loading-spinner';

export default function DashboardPage() {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.replace('/login'); // Redirect to login if not authenticated
      } else {
        // If authenticated, redirect to the main todo app page
        router.replace('/');
      }
    }
  }, [user, loading, router]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <LoadingSpinner size="lg" />
      <h1 className="text-2xl font-bold mt-4">Redirecting...</h1>
      <p className="mt-2 text-gray-500">Loading your todo app...</p>
    </div>
  );
}
