# jwt-middleware-generator

## Purpose
Generate secure JWT verification middleware for FastAPI

## Responsibilities
- Create middleware to validate JWT tokens
- Extract and verify token claims securely
- Handle token expiration and refresh scenarios
- Integrate with authentication providers
- Log security events appropriately

## Inputs
- JWT signing algorithm and secret/key configuration
- Token claim requirements and validation rules
- Authentication provider settings
- Security logging preferences

## Outputs
- FastAPI middleware class for JWT verification
- Token validation functions with error handling
- Configuration setup for middleware integration
- Security event logging mechanisms

## Rules
- NEVER expose secret keys in generated code
- NEVER bypass security validations
- NEVER store sensitive data insecurely
- ALWAYS follow security best practices for token handling

## When to use this skill
Use when implementing authentication systems, securing API endpoints, or adding JWT-based authorization to FastAPI applications.