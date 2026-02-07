# JWT Authentication Manager - Memory

## Backend Authentication Flow

### Token Generation (Fixed)
- **Issue Found**: `/auth/login` and `/auth/register` endpoints were only returning `access_token`
- **Fix Applied**: Updated both endpoints to return both `access_token` and `refresh_token`
- **Location**: `/backend/routes/auth.py`
- **Token Functions**: Using `core.security.create_access_token()` and `create_refresh_token()`

### Token Response Structure
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "access_token": "jwt-token",
  "refresh_token": "jwt-token",
  "token_type": "bearer"
}
```

### Token Refresh Endpoint
- **Added**: `POST /auth/refresh` endpoint
- **Purpose**: Exchange refresh token for new access token
- **Request**: `{"refresh_token": "token"}`
- **Response**: `{"access_token": "new-token", "token_type": "bearer"}`

## Frontend Token Storage

### Token Management (`/frontend/src/lib/token.ts`)
- Stores tokens in `localStorage`
- Keys: `access_token` and `refresh_token`
- Functions: `getAccessToken()`, `getRefreshToken()`, `setTokens()`, `clearTokens()`

### API Client (`/frontend/src/services/api.ts`)
- Axios interceptor attaches Bearer token to all requests
- Automatic token refresh on 401 responses
- Request queuing during refresh to prevent race conditions
- Redirect to `/login` if refresh fails

### Auth Service (`/frontend/src/services/auth.service.ts`)
- `login()` and `register()` both store tokens via `setTokens()`
- **Previous Issue**: Expected both tokens but backend only returned `access_token`
- **Now Fixed**: Backend returns both tokens as expected

## Protected Routes

### Chat Endpoint (`POST /api/chat/message`)
- **Protection**: `Depends(get_current_user)` middleware
- **Auth Method**: `HTTPBearer` security scheme
- **User Extraction**: JWT `sub` claim contains user ID
- **CORS**: Configured with `allow_origins=["*"]` in development

## Security Checklist Status
- [x] Passwords hashed with bcrypt (SHA-256 normalized)
- [x] JWT secrets in `.env` file
- [x] Access tokens expire (60 minutes configured)
- [x] Refresh tokens expire (7 days configured)
- [x] Token validation checks signature, expiration, and claims
- [x] CORS configured for frontend communication
- [x] Bearer token authentication on protected routes

## Common Issues & Solutions

### "Unable to connect" Error
**Cause**: Frontend couldn't authenticate because backend wasn't returning `refresh_token`
**Solution**: Updated `/auth/login` and `/auth/register` to include `refresh_token` in response

### Token Storage
**Current**: localStorage (acceptable for this app)
**Production Recommendation**: Use httpOnly cookies for refresh tokens to prevent XSS attacks

### CORS Configuration
- **Development**: `allow_origins=["*"]` with `allow_credentials=True`
- **Production**: Replace with specific frontend origin (e.g., `["https://yourdomain.com"]`)

## File Locations
- **Backend Auth Routes**: `/backend/routes/auth.py`
- **Security Functions**: `/backend/core/security.py`
- **Password Hashing**: `/backend/utils/auth.py`
- **Frontend API Client**: `/frontend/src/services/api.ts`
- **Token Management**: `/frontend/src/lib/token.ts`
- **Auth Service**: `/frontend/src/services/auth.service.ts`
