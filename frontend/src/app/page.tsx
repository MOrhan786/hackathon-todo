'use client';

import { useAuth } from '@/hooks/useAuth';
import DashboardHome from '@/components/dashboard/DashboardHome';
import LandingPage from '@/components/landing/LandingPage';
import LoadingSpinner from '@/components/ui/loading-spinner';

export default function HomePage() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-background">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return user ? <DashboardHome /> : <LandingPage />;
}
