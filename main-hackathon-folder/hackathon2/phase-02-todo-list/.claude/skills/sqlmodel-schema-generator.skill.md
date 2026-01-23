# sqlmodel-schema-generator

## Purpose
Create optimized SQLModel database schemas with indexes and constraints

## Responsibilities
- Generate SQLModel class definitions from requirements
- Create appropriate relationships between models
- Define proper indexing strategies for performance
- Add necessary constraints and validation rules
- Ensure referential integrity across tables

## Inputs
- Entity requirements and attributes
- Relationship definitions between entities
- Performance requirements and query patterns
- Database optimization constraints

## Outputs
- SQLModel class definitions with proper typing
- Relationship mappings and foreign key constraints
- Index specifications for optimal queries
- Migration scripts for schema implementation
- Documentation of schema structure

## Rules
- NEVER create schemas without proper normalization
- NEVER omit critical constraints or validations
- NEVER ignore performance implications of design choices
- ALWAYS maintain data integrity across relationships

## When to use this skill
Use when designing database schemas, creating data models, or defining persistent storage structures for applications.