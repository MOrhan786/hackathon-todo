---
name: spec-validator
description: "Validate spec completeness and quality. Validates chatbot interactions, task management operations, and language understanding features to ensure specifications meet quality standards."
version: "1.0.0"
used_by:
  - Constitution-Keeper
  - Orchestrator
  - Chatbot AI Agent
tags:
  - validation
  - quality
  - specification
  - chatbot
---

# Spec Validator Skill

## Purpose

Validate specification completeness and quality to ensure all project documentation meets defined standards. This includes validating chatbot interactions, task management operations, and natural language understanding features.

## Capabilities

### 1. Structural Validation
- Verify all mandatory sections are present
- Check section ordering follows template
- Validate markdown formatting
- Ensure proper heading hierarchy

### 2. Content Quality Validation
- Check for implementation details (should be absent)
- Verify focus on user value and business needs
- Ensure language is accessible to non-technical stakeholders
- Validate clarity and unambiguity of requirements

### 3. Requirements Validation
- Verify each requirement is testable
- Check for measurable acceptance criteria
- Validate success criteria are technology-agnostic
- Ensure requirements are complete and non-contradictory

### 4. Chatbot Validation
- Validate intent definitions are complete
- Check trigger phrases have sufficient variety
- Verify entity extraction rules are defined
- Validate conversation flows are complete
- Check error handling patterns exist

### 5. Task Management Validation
- Validate CRUD operations are fully specified
- Check state transitions are defined
- Verify notification requirements are complete
- Validate recurring task patterns

## Validation Rules

### Mandatory Section Rules
```yaml
required_sections:
  - overview: true
  - user_types: true
  - functional_requirements: true
  - success_criteria: true
  - user_scenarios: true

optional_sections:
  - ui_ux_requirements: "if UI feature"
  - chatbot_interactions: "if chatbot feature"
  - key_entities: "if data involved"
  - assumptions: true
  - constraints: true
```

### Content Quality Rules
```yaml
quality_checks:
  no_implementation_details:
    patterns_to_flag:
      - "React|Vue|Angular"
      - "Python|JavaScript|TypeScript"
      - "PostgreSQL|MySQL|MongoDB"
      - "API endpoint|REST|GraphQL"
      - "database|query|index"
    severity: error

  testable_requirements:
    must_have:
      - measurable_outcome: true
      - clear_conditions: true
      - defined_actors: true
    severity: error

  technology_agnostic_criteria:
    patterns_to_flag:
      - "ms|milliseconds|latency"
      - "TPS|transactions per second"
      - "cache hit|query time"
    severity: warning
```

### Chatbot Validation Rules
```yaml
chatbot_checks:
  intent_completeness:
    required:
      - trigger_phrases: "min 3 examples"
      - entities: "if applicable"
      - response_pattern: true
      - error_handling: true
    severity: error

  conversation_flow:
    required:
      - entry_points: true
      - transitions: true
      - exit_conditions: true
    severity: error

  nlp_requirements:
    required:
      - entity_types: true
      - extraction_rules: true
      - validation_rules: true
    severity: warning
```

### Task Management Validation Rules
```yaml
task_management_checks:
  crud_operations:
    required:
      - create: "with validation rules"
      - read: "with filtering options"
      - update: "with partial update support"
      - delete: "with confirmation/undo"
    severity: error

  state_management:
    required:
      - states_defined: true
      - transitions_documented: true
      - persistence_rules: true
    severity: error
```

## Validation Output Format

### Validation Report
```json
{
  "file": "specs/feature/spec.md",
  "timestamp": "ISO-date",
  "status": "pass|fail|warning",
  "summary": {
    "total_checks": 25,
    "passed": 22,
    "failed": 2,
    "warnings": 1
  },
  "results": [
    {
      "rule": "no_implementation_details",
      "status": "fail",
      "severity": "error",
      "location": "line 45",
      "message": "Implementation detail found: 'PostgreSQL'",
      "suggestion": "Replace with technology-agnostic description"
    }
  ],
  "recommendations": [
    "Remove database technology references",
    "Add more trigger phrases for 'create_task' intent"
  ]
}
```

### Checklist Output
```markdown
# Specification Validation Checklist

## Structural Validation
- [x] All mandatory sections present
- [x] Section ordering correct
- [x] Markdown formatting valid
- [ ] Proper heading hierarchy

## Content Quality
- [x] No implementation details
- [x] User-focused language
- [ ] Non-technical accessibility

## Requirements Quality
- [x] Requirements testable
- [x] Acceptance criteria measurable
- [x] Success criteria technology-agnostic

## Chatbot Validation
- [x] Intents complete
- [ ] Trigger phrases sufficient (3 minimum)
- [x] Entity extraction defined
- [x] Error handling present

## Task Management Validation
- [x] CRUD operations specified
- [x] State transitions defined
- [ ] Notification requirements complete
```

## Usage Examples

### Validating a Feature Specification
```
Input: Validate specs/user-auth/spec.md

Output:
- Status: PASS with warnings
- 23/25 checks passed
- 2 warnings:
  - Line 67: Consider adding more user scenarios
  - Line 89: Success criteria could be more specific
```

### Validating Chatbot Features
```
Input: Validate chatbot interactions in specs/task-chatbot/spec.md

Output:
- Status: FAIL
- Issues:
  - Intent 'delete_task' missing error handling
  - Insufficient trigger phrases for 'mark_complete' (2 found, 3 required)
  - Entity 'due_date' missing extraction rules
```

### Validating Task Management
```
Input: Validate task management operations

Output:
- Status: PASS
- All CRUD operations specified
- State transitions documented
- Notifications defined
```

## Error Handling

- Gracefully handles missing files
- Reports partial validation if file is incomplete
- Provides actionable suggestions for each failure
- Distinguishes between errors (blocking) and warnings (advisory)

## Integration Points

- Works with Spec-Reader to access specifications
- Feeds validation results to Spec-Writer for corrections
- Provides quality gate for Plan generation
- Integrates with Constitution-Keeper for standards enforcement
