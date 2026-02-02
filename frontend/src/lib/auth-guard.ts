'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

// Check if user is authenticated by checking for token in cookies/localStorage
export function requireAuth(redirectPath: string = '/login'): void {
  // For client-side, we can't use cookies directly, so this function is conceptual
  // The actual auth guard will be implemented in the component
}

// For client-side authentication check
export function isAuthenticatedClient(): boolean {
  if (typeof window === 'undefined') {
    return false; // Not running in browser
  }

  const token = localStorage.getItem('access_token');
  if (!token) {
    return false;
  }

  // Check if token is expired (decode JWT and check exp claim)
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp > currentTime;
  } catch (error) {
    return false;
  }
}