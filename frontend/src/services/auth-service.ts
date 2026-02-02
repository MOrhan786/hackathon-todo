import { User, UserCredentials, UserRegistration } from '@/types/user';
import { authApiService } from './auth-api-service';

// Authentication service with additional utility functions
export const authService = {
  // Register a new user
  async register(userData: UserRegistration): Promise<User> {
    return await authApiService.register(userData);
  },

  // Login user
  async login(credentials: UserCredentials): Promise<User> {
    // The authApiService.login already stores the token
    await authApiService.login(credentials);

    // Get user info from the token
    return this.getCurrentUser() as User;
  },

  // Logout user
  async logout(): Promise<void> {
    return await authApiService.logout();
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token');
    if (!token) {
      return false;
    }

    // Check if token is expired (decode JWT and check exp claim)
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      // If exp is missing or invalid, treat user as authenticated
      if (!payload.exp) {
        return true;
      }
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch (error) {
      // If there's an error decoding the token, just check if it exists
      return !!token;
    }
  },

  // Get JWT token
  getToken(): string | null {
    return localStorage.getItem('access_token');
  },

  // Get user info (could be extended to fetch from backend)
  getCurrentUser(): User | null {
    const token = this.getToken();
    if (!token) {
      return null;
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      // Extract user info from JWT payload (contains sub which is user ID)
      return {
        id: payload.sub || '',
        email: payload.email || '', // Email might not be in the token
        created_at: payload.iat ? new Date(payload.iat * 1000).toISOString() : '',
        updated_at: payload.exp ? new Date(payload.exp * 1000).toISOString() : ''
      };
    } catch (error) {
      console.error('Error parsing token:', error);
      return null;
    }
  }
};