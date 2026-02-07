'use client';

// Authentication Context Provider

import React, { createContext, useState, useEffect, useCallback } from 'react';
import { User } from '@/types/auth.types';
import { getAccessToken, clearTokens } from '@/lib/token';
import authService from '@/services/auth.service';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
}

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Helper function to decode JWT and extract user info
  const getUserFromToken = (token: string): User | null => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));

      // Check if token is expired
      if (payload.exp && payload.exp < Date.now() / 1000) {
        return null;
      }

      // Extract user info from JWT payload
      return {
        id: payload.sub || '',
        email: payload.email || '',
        created_at: payload.iat ? new Date(payload.iat * 1000).toISOString() : new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  };

  // Verify token and fetch user data on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = getAccessToken();
      if (token) {
        try {
          // Decode token and extract user info
          const userData = getUserFromToken(token);

          if (userData) {
            setUser(userData);
          } else {
            // Token is invalid or expired
            clearTokens();
            setUser(null);
          }
        } catch (error) {
          console.error('Token verification failed:', error);
          clearTokens();
          setUser(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await authService.login(email, password);
    setUser({
      id: response.id,
      email: response.email,
      created_at: response.created_at,
      updated_at: response.updated_at,
    });
  }, []);

  const register = useCallback(async (email: string, password: string) => {
    const response = await authService.register(email, password);
    setUser({
      id: response.id,
      email: response.email,
      created_at: response.created_at,
      updated_at: response.updated_at,
    });
  }, []);

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  }, []);

  const refreshToken = useCallback(async (): Promise<boolean> => {
    // Token refresh is handled by Axios interceptor in api.ts
    // This is just a manual trigger if needed
    return false;
  }, []);

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    refreshToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
