'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth-service';

export default function DashboardPage() {
  const router = useRouter();

  useEffect(() => {
    // Agar user login nahi hai → login page
    if (!authService.isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold">✅ Welcome to Dashboard</h1>
      <p className="mt-2 text-gray-500">Login successful 🎉</p>
    </div>
  );
}
