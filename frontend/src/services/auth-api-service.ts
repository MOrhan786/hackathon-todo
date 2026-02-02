import { User, UserCredentials, UserRegistration } from '@/types/user';

// Base API URL - defaults to localhost:8000 for development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Define types for authentication responses
interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface RegistrationResponse extends LoginResponse {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

// Authentication API service
export const authApiService = {
  // Register a new user
  async register(userData: UserRegistration): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data: RegistrationResponse = await response.json();

      // Store the JWT token in localStorage
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
      }

      // Return user data
      return {
        id: data.id,
        email: data.email,
        created_at: data.created_at,
        updated_at: data.updated_at,
      };
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Login user
  async login(credentials: UserCredentials): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data: LoginResponse = await response.json();

      // Store the JWT token in localStorage
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
      }

      // Since login only returns token, we need to get user info separately
      // For now, we'll return a minimal user object and get full user info in a separate call if needed
      return {
        id: '', // Will be populated later when we fetch user details
        email: credentials.email,
        created_at: '',
        updated_at: ''
      };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Logout user
  async logout(): Promise<void> {
    try {
      // Get the token before clearing it
      const token = localStorage.getItem('access_token');

      // Remove token from localStorage
      localStorage.removeItem('access_token');

      // Optionally call backend logout endpoint
      if (token) {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }).catch(() => {
          // Ignore logout errors - this is fine as logout is best-effort
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
      // Still remove the token locally even if the API call fails
      localStorage.removeItem('access_token');
    }
  }
};