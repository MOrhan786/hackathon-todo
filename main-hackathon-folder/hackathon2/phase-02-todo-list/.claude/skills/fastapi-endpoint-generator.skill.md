# fastapi-endpoint-generator

## Purpose
Generate production-ready FastAPI endpoints with validation and error handling

## Responsibilities
- Create endpoint functions with proper request/response models
- Implement input validation using Pydantic models
- Add comprehensive error handling and status codes
- Generate API documentation automatically
- Include rate limiting and security measures

## Inputs
- Endpoint requirements and HTTP method
- Request/response data models
- Authentication and authorization requirements
- Business logic specifications

## Outputs
- Complete FastAPI endpoint with path operations
- Pydantic models for request/response validation
- Error response definitions
- OpenAPI documentation components
- Security configurations

## Rules
- NEVER create endpoints without input validation
- NEVER ignore error handling requirements
- NEVER expose sensitive data in responses
- ALWAYS follow REST API best practices

## When to use this skill
Use when developing API endpoints, creating service layers, or implementing backend functionality in FastAPI applications.