---
name: spec-reader
description: "Read and parse all spec-kit plus files including specifications, plans, tasks, and chatbot-related artifacts. Provides structured access to project documentation for orchestration, spec management, and chatbot functionality."
version: "1.0.0"
used_by:
  - Orchestrator
  - Spec-Manager
  - Constitution-Keeper
  - Chatbot AI Agent
tags:
  - specification
  - parsing
  - documentation
  - chatbot
---

# Spec Reader Skill

## Purpose

Read and parse all spec-kit plus files to provide structured access to project documentation. This skill enables agents to understand feature specifications, implementation plans, task lists, and chatbot-related configurations.

## Capabilities

### 1. Specification File Parsing
- Read and parse `specs/<feature>/spec.md` files
- Extract feature requirements, success criteria, and acceptance scenarios
- Identify user scenarios and functional requirements
- Parse key entities and data structures

### 2. Plan File Parsing
- Read and parse `specs/<feature>/plan.md` files
- Extract architectural decisions and technical approaches
- Identify dependencies and integration points
- Parse API contracts and interface definitions

### 3. Task File Parsing
- Read and parse `specs/<feature>/tasks.md` files
- Extract individual tasks with their acceptance criteria
- Parse task dependencies and ordering
- Identify test cases for each task

### 4. Constitution Parsing
- Read and parse `.specify/memory/constitution.md`
- Extract project principles and coding standards
- Parse security, performance, and testing guidelines
- Identify architectural patterns and constraints

### 5. Chatbot-Related Parsing
- Parse natural language processing feature specifications
- Extract chatbot conversation flows and intents
- Identify task management commands for chatbot
- Parse user interaction patterns

## Input Formats

### File Types Supported
- `.md` - Markdown specification files
- `.prompt.md` - Prompt history records
- `.yaml/.yml` - Configuration files
- `.json` - JSON-based specifications

### Directory Structure
```
specs/
  <feature-name>/
    spec.md          # Feature specification
    plan.md          # Implementation plan
    tasks.md         # Task breakdown
    checklists/      # Validation checklists
.specify/
  memory/
    constitution.md  # Project principles
  templates/         # Document templates
history/
  prompts/           # Prompt history records
  adr/              # Architecture decision records
```

## Output Format

### Parsed Specification Object
```json
{
  "feature": "feature-name",
  "title": "Feature Title",
  "status": "draft|review|approved",
  "sections": {
    "overview": "...",
    "requirements": [...],
    "success_criteria": [...],
    "user_scenarios": [...],
    "entities": [...],
    "assumptions": [...],
    "constraints": [...]
  },
  "metadata": {
    "created": "ISO-date",
    "updated": "ISO-date",
    "version": "1.0.0"
  }
}
```

### Parsed Plan Object
```json
{
  "feature": "feature-name",
  "architecture": {...},
  "decisions": [...],
  "interfaces": [...],
  "dependencies": [...],
  "risks": [...]
}
```

### Parsed Tasks Object
```json
{
  "feature": "feature-name",
  "tasks": [
    {
      "id": "TASK-001",
      "title": "...",
      "status": "pending|in_progress|completed",
      "acceptance_criteria": [...],
      "dependencies": [...],
      "test_cases": [...]
    }
  ]
}
```

## Usage Examples

### Reading a Feature Specification
```
Input: Read spec for "user-authentication" feature
Output: Parsed specification object with all sections
```

### Reading All Tasks for a Feature
```
Input: Get all tasks for "chatbot-integration" feature
Output: List of parsed task objects with status and dependencies
```

### Reading Constitution Principles
```
Input: Get coding standards from constitution
Output: Structured list of principles and guidelines
```

### Reading Chatbot Configuration
```
Input: Parse chatbot conversation flows
Output: Structured intents, entities, and response patterns
```

## Error Handling

- Returns structured error if file not found
- Validates file format before parsing
- Reports incomplete or malformed sections
- Suggests corrections for common formatting issues

## Integration Points

- Works with Spec-Writer for creating new specifications
- Integrates with Spec-Validator for quality checks
- Provides data to Chatbot AI Agent for understanding context
- Feeds Orchestrator with project state information
