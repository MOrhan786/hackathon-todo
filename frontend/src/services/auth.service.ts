// Authentication Service

import api from './api';
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  RefreshTokenRequest,
  RefreshTokenResponse,
} from '@/types/auth.types';
import { setTokens } from '@/lib/token';

class AuthService {
  /**
   * Register a new user
   */
  async register(email: string, password: string): Promise<RegisterResponse> {
    const payload: RegisterRequest = { email, password };
    const response = await api.post<RegisterResponse>('/auth/register', payload);

    // Store tokens
    const { access_token, refresh_token } = response.data;
    setTokens(access_token, refresh_token);

    return response.data;
  }

  /**
   * Login existing user
   */
  async login(email: string, password: string): Promise<LoginResponse> {
    const payload: LoginRequest = { email, password };
    const response = await api.post<LoginResponse>('/auth/login', payload);

    // Store tokens
    const { access_token, refresh_token } = response.data;
    setTokens(access_token, refresh_token);

    return response.data;
  }

  /**
   * Refresh access token using refresh token
   */
  async refresh(refreshToken: string): Promise<RefreshTokenResponse> {
    const payload: RefreshTokenRequest = { refresh_token: refreshToken };
    const response = await api.post<RefreshTokenResponse>('/auth/refresh', payload);
    return response.data;
  }

  /**
   * Logout (client-side token clearing)
   */
  async logout(): Promise<void> {
    try {
      // Optional: Call backend logout endpoint if it exists
      await api.post('/auth/logout');
    } catch (error) {
      // Ignore errors, just clear tokens client-side
      console.warn('Logout API call failed, clearing tokens anyway');
    }
  }
}

export default new AuthService();
