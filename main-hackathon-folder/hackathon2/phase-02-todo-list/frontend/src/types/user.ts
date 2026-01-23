// User interface
export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

// User registration data
export interface UserRegistration {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

// User login credentials
export interface UserCredentials {
  email: string;
  password: string;
}

// User response from API
export interface UserResponse {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
  access_token?: string;
  token_type?: string;
}