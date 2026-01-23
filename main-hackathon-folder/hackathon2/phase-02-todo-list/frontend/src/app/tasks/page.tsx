'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function TasksRedirectPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the main dashboard page which shows tasks
    router.push('/');
  }, [router]);

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
    </div>
  );
}