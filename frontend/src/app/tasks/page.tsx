'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth-service';

export default function TasksRedirectPage() {
  const router = useRouter();

  useEffect(() => {
    // Check authentication before redirecting
    if (authService.isAuthenticated()) {
      // Redirect to the main dashboard page which shows tasks
      router.replace('/');
    } else {
      // If not authenticated, go to login
      router.replace('/login');
    }
  }, [router]);

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
    </div>
  );
}