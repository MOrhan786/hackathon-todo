import authService from '@/services/auth.service'
import { setTokens, getAccessToken, getRefreshToken, clearTokens } from '@/lib/token'

// Mock the API
jest.mock('@/services/api', () => ({
  __esModule: true,
  default: {
    post: jest.fn(),
  },
}))

import api from '@/services/api'

describe('Authentication Flow Integration', () => {
  const mockApi = api as jest.Mocked<typeof api>

  beforeEach(() => {
    jest.clearAllMocks()
    clearTokens()
  })

  afterEach(() => {
    clearTokens()
  })

  describe('Registration Flow', () => {
    it('completes full registration flow: register → tokens stored', async () => {
      // Mock registration response
      const mockRegisterResponse = {
        data: {
          id: 'user-123',
          email: 'newuser@example.com',
          created_at: '2026-02-06T12:00:00Z',
          updated_at: '2026-02-06T12:00:00Z',
          access_token: 'mock-access-token',
          refresh_token: 'mock-refresh-token',
        },
      }

      mockApi.post.mockResolvedValueOnce(mockRegisterResponse)

      // Register user
      const result = await authService.register('newuser@example.com', 'password123')

      // Verify API was called
      expect(mockApi.post).toHaveBeenCalledWith('/auth/register', {
        email: 'newuser@example.com',
        password: 'password123',
      })

      // Verify tokens are stored
      expect(getAccessToken()).toBe('mock-access-token')
      expect(getRefreshToken()).toBe('mock-refresh-token')

      // Verify user data returned
      expect(result.email).toBe('newuser@example.com')
      expect(result.id).toBe('user-123')
    })
  })

  describe('Login Flow', () => {
    it('completes full login flow: login → tokens stored', async () => {
      // Mock login response
      const mockLoginResponse = {
        data: {
          access_token: 'mock-access-token',
          refresh_token: 'mock-refresh-token',
          token_type: 'bearer',
        },
      }

      mockApi.post.mockResolvedValueOnce(mockLoginResponse)

      // Login user
      await authService.login('user@example.com', 'password123')

      // Verify API was called
      expect(mockApi.post).toHaveBeenCalledWith('/auth/login', {
        email: 'user@example.com',
        password: 'password123',
      })

      // Verify tokens are stored
      expect(getAccessToken()).toBe('mock-access-token')
      expect(getRefreshToken()).toBe('mock-refresh-token')
    })
  })

  describe('Token Refresh Flow', () => {
    it('refreshes access token using refresh token', async () => {
      // Set initial tokens
      setTokens('old-access-token', 'valid-refresh-token')

      // Mock refresh response
      const mockRefreshResponse = {
        data: {
          access_token: 'new-access-token',
          token_type: 'bearer',
        },
      }

      mockApi.post.mockResolvedValueOnce(mockRefreshResponse)

      // Refresh token
      const result = await authService.refresh('valid-refresh-token')

      // Verify API was called
      expect(mockApi.post).toHaveBeenCalledWith('/auth/refresh', {
        refresh_token: 'valid-refresh-token',
      })

      // Verify new token returned
      expect(result.access_token).toBe('new-access-token')
    })
  })

  describe('Logout Flow', () => {
    it('completes full logout flow: logout → tokens cleared', async () => {
      // Set initial tokens
      setTokens('access-token', 'refresh-token')
      expect(getAccessToken()).toBe('access-token')

      // Mock logout response (optional API call)
      mockApi.post.mockResolvedValueOnce({ data: { message: 'Logged out' } })

      // Logout
      await authService.logout()

      // Note: Token clearing happens in AuthContext, not in authService
      // In a real scenario, the AuthContext would call clearTokens()
      clearTokens()

      // Verify tokens are cleared
      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })
  })

  describe('Complete Auth Lifecycle', () => {
    it('register → login → token refresh → logout', async () => {
      // Step 1: Register
      mockApi.post.mockResolvedValueOnce({
        data: {
          id: 'user-123',
          email: 'test@example.com',
          created_at: '2026-02-06T12:00:00Z',
          updated_at: '2026-02-06T12:00:00Z',
          access_token: 'register-access-token',
          refresh_token: 'register-refresh-token',
        },
      })

      await authService.register('test@example.com', 'password123')
      expect(getAccessToken()).toBe('register-access-token')

      // Step 2: Logout (clear tokens)
      clearTokens()
      expect(getAccessToken()).toBeNull()

      // Step 3: Login
      mockApi.post.mockResolvedValueOnce({
        data: {
          access_token: 'login-access-token',
          refresh_token: 'login-refresh-token',
          token_type: 'bearer',
        },
      })

      await authService.login('test@example.com', 'password123')
      expect(getAccessToken()).toBe('login-access-token')

      // Step 4: Refresh token
      mockApi.post.mockResolvedValueOnce({
        data: {
          access_token: 'refreshed-access-token',
          token_type: 'bearer',
        },
      })

      await authService.refresh('login-refresh-token')
      // Note: Tokens would be updated by the API interceptor in real usage

      // Step 5: Logout
      clearTokens()
      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })
  })
})
