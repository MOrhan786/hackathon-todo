// Authentication Types

export interface User {
  id: string; // UUID as string
  email: string;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

export interface AuthTokens {
  access_token: string; // JWT access token
  refresh_token: string; // JWT refresh token
  token_type: 'bearer';
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginResponse extends User {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

export interface RegisterResponse extends LoginResponse {
  // Same as LoginResponse
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: 'bearer';
}
