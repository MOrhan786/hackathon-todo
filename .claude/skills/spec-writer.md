---
name: spec-writer
description: "Create detailed specifications with UI/UX requirements. Handles user interactions and task management features for the chatbot, ensuring comprehensive documentation of functional and non-functional requirements."
version: "1.0.0"
used_by:
  - Spec-Manager
  - Chatbot AI Agent
tags:
  - specification
  - documentation
  - ui-ux
  - chatbot
---

# Spec Writer Skill

## Purpose

Create detailed specifications with comprehensive UI/UX requirements. This skill enables the creation of high-quality feature specifications that include user interactions, task management features, and chatbot functionality documentation.

## Capabilities

### 1. Feature Specification Creation
- Generate complete feature specifications from natural language descriptions
- Structure specifications using the standard template
- Include all mandatory sections (overview, requirements, success criteria)
- Add optional sections when relevant to the feature

### 2. UI/UX Requirements Documentation
- Document user interface components and layouts
- Specify user interaction patterns and flows
- Define responsive design requirements
- Include accessibility considerations (WCAG compliance)

### 3. User Scenario Development
- Create detailed user scenarios and workflows
- Document happy path and edge case scenarios
- Define acceptance criteria for each scenario
- Include testing considerations

### 4. Chatbot Interaction Specifications
- Document conversational UI requirements
- Specify natural language understanding patterns
- Define chatbot response formats and tones
- Document task management commands and syntax

### 5. Task Management Feature Specs
- Specify task CRUD operations
- Document task state transitions
- Define reminder and notification requirements
- Specify recurring task patterns

## Input Requirements

### Feature Description Format
```
Feature: [Feature Name]
Description: [Natural language description]
User Types: [List of user roles]
Priority: [High/Medium/Low]
```

### UI/UX Input
```
Screens: [List of screens/views]
Components: [Key UI components]
Interactions: [User actions]
Responsive: [Breakpoints/devices]
```

## Output Format

### Specification Document Structure
```markdown
# Feature: [Name]

## Overview
[Brief description of the feature and its value]

## User Types
- [User type 1]: [Description and permissions]
- [User type 2]: [Description and permissions]

## Functional Requirements

### FR-001: [Requirement Title]
**Description**: [What the system must do]
**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

## UI/UX Requirements

### Screen: [Screen Name]
**Layout**: [Description]
**Components**:
- Component 1: [Specifications]
- Component 2: [Specifications]

**Interactions**:
- Action 1 → Result 1
- Action 2 → Result 2

**Responsive Behavior**:
- Mobile: [Behavior]
- Tablet: [Behavior]
- Desktop: [Behavior]

## User Scenarios

### Scenario 1: [Title]
**Given**: [Preconditions]
**When**: [User actions]
**Then**: [Expected outcomes]

## Success Criteria
- [ ] Measurable outcome 1
- [ ] Measurable outcome 2

## Assumptions
- Assumption 1
- Assumption 2

## Constraints
- Constraint 1
- Constraint 2
```

## Chatbot-Specific Sections

### Conversation Flow Documentation
```markdown
## Chatbot Interactions

### Intent: [Intent Name]
**Trigger Phrases**:
- "phrase 1"
- "phrase 2"

**Required Entities**:
- entity_name: [type]

**Response Pattern**:
```
[Response template with {placeholders}]
```

**Follow-up Actions**:
- Action 1
- Action 2
```

### Task Command Documentation
```markdown
## Task Management Commands

### Command: Create Task
**Syntax**: "Add/Create [task description] [optional: due date]"
**Examples**:
- "Add buy groceries to my list"
- "Create a task for tomorrow: call mom"

**Validation**:
- Task description: required, min 3 characters
- Due date: optional, parseable date format

**Response**:
- Success: "Created task: {task_title}"
- Error: "Could not create task: {reason}"
```

## Quality Guidelines

### Specification Quality Checklist
- [ ] No implementation details (languages, frameworks)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic

### UI/UX Documentation Quality
- [ ] All screens/views documented
- [ ] Interaction patterns clearly defined
- [ ] Responsive breakpoints specified
- [ ] Accessibility requirements included
- [ ] Error states documented

### Chatbot Specification Quality
- [ ] All intents documented with examples
- [ ] Entity extraction rules defined
- [ ] Response patterns include error handling
- [ ] Conversation flows are complete
- [ ] Edge cases handled

## Usage Examples

### Creating a Task Management Feature Spec
```
Input: "Users should be able to create, view, edit, and delete tasks with due dates and priorities"

Output: Complete specification including:
- CRUD requirements for tasks
- UI components for task list and forms
- User scenarios for each operation
- Success criteria for task management
```

### Creating a Chatbot Feature Spec
```
Input: "Chatbot should understand natural language commands for managing tasks"

Output: Complete specification including:
- Intent definitions with trigger phrases
- Entity extraction requirements
- Response patterns for success/failure
- Conversation flow diagrams
```

## Error Handling

- Validates input completeness before generation
- Flags ambiguous requirements with [NEEDS CLARIFICATION]
- Limits clarification markers to 3 maximum
- Provides suggested answers for ambiguous items

## Integration Points

- Uses Spec-Reader to check existing specifications
- Integrates with Spec-Validator for quality validation
- Feeds into Plan generation workflow
- Provides foundation for Task generation
