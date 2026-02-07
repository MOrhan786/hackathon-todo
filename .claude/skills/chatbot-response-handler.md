---
name: chatbot-response-handler
description: "Handle and parse responses from the chatbot AI. Parses user inputs, provides structured responses, and manages chatbot conversation state for seamless task management interactions."
version: "1.0.0"
used_by:
  - Chatbot AI Agent
tags:
  - chatbot
  - nlp
  - conversation
  - response
---

# Chatbot Response Handler Skill

## Purpose

Handle and parse responses from the chatbot AI to provide a seamless conversational experience. This skill parses user inputs, generates structured responses, and manages conversation state for effective task management interactions.

## Capabilities

### 1. Input Parsing
- Parse natural language user messages
- Extract intents from user input
- Identify entities (dates, task names, priorities)
- Handle multi-turn conversations

### 2. Response Generation
- Generate contextual responses
- Format task information for display
- Create confirmation messages
- Provide helpful suggestions

### 3. Conversation State Management
- Track conversation context
- Maintain session state
- Handle conversation branches
- Manage clarification flows

### 4. Task Action Coordination
- Translate intents to task operations
- Validate task parameters
- Execute task CRUD operations
- Report operation results

### 5. Error Recovery
- Handle misunderstood inputs
- Provide clarification requests
- Offer fallback responses
- Guide users to valid commands

## Intent Definitions

### Task Management Intents
```yaml
intents:
  create_task:
    description: "User wants to create a new task"
    examples:
      - "Add buy groceries to my list"
      - "Create a task for tomorrow"
      - "Remind me to call mom"
      - "I need to finish the report"
    required_entities:
      - task_title
    optional_entities:
      - due_date
      - priority
      - tags
    response_pattern: |
      Created task: "{task_title}"
      {if due_date}Due: {due_date}{/if}
      {if priority}Priority: {priority}{/if}

  list_tasks:
    description: "User wants to see their tasks"
    examples:
      - "Show my tasks"
      - "What do I have to do?"
      - "List all my tasks"
      - "What's on my list?"
    optional_entities:
      - status_filter
      - date_filter
      - priority_filter
    response_pattern: |
      Here are your {filter_description}tasks:
      {for task in tasks}
      - [{status_icon}] {task.title} {if task.due_date}(due {task.due_date}){/if}
      {/for}

  complete_task:
    description: "User wants to mark a task as complete"
    examples:
      - "Mark buy groceries as done"
      - "I finished the report"
      - "Complete the first task"
      - "Done with shopping"
    required_entities:
      - task_reference
    response_pattern: |
      Marked as complete: "{task_title}"

  delete_task:
    description: "User wants to delete a task"
    examples:
      - "Delete the shopping task"
      - "Remove buy groceries"
      - "Cancel the meeting reminder"
    required_entities:
      - task_reference
    confirmation_required: true
    response_pattern: |
      Deleted: "{task_title}"

  update_task:
    description: "User wants to modify a task"
    examples:
      - "Change the deadline to Friday"
      - "Set priority to high for the report"
      - "Rename shopping to grocery shopping"
    required_entities:
      - task_reference
      - update_field
      - new_value
    response_pattern: |
      Updated "{task_title}": {update_field} → {new_value}

  search_tasks:
    description: "User wants to find specific tasks"
    examples:
      - "Find tasks about shopping"
      - "Search for meeting"
      - "Which tasks are due tomorrow?"
    required_entities:
      - search_query
    response_pattern: |
      Found {count} task(s) matching "{search_query}":
      {for task in results}
      - {task.title}
      {/for}

  help:
    description: "User needs help or guidance"
    examples:
      - "What can you do?"
      - "Help"
      - "How do I create a task?"
    response_pattern: |
      I can help you manage your tasks! Try:
      - "Add [task name]" to create a task
      - "Show my tasks" to see your list
      - "Mark [task] as done" to complete
      - "Delete [task]" to remove

  greeting:
    description: "User greets the chatbot"
    examples:
      - "Hello"
      - "Hi"
      - "Hey"
    response_pattern: |
      Hi there! How can I help with your tasks today?
```

### Entity Definitions
```yaml
entities:
  task_title:
    type: string
    extraction:
      - pattern: "add (.+) to my list"
      - pattern: "create (?:a )?task (?:called |named |for )?(.+)"
      - pattern: "remind me to (.+)"
    validation:
      min_length: 1
      max_length: 255

  due_date:
    type: datetime
    extraction:
      - pattern: "(?:by |due |for |on )(.+)"
      - named_entities: ["tomorrow", "today", "next week", "monday", etc.]
    formats:
      - relative: ["tomorrow", "in 2 days", "next week"]
      - absolute: ["January 15", "01/15/2024", "2024-01-15"]

  priority:
    type: enum
    values: ["low", "medium", "high", "urgent"]
    extraction:
      - pattern: "(?:priority|important|urgent)(?:: )?(\w+)"
      - indicators:
          urgent: ["urgent", "asap", "immediately"]
          high: ["important", "high priority", "critical"]
          low: ["low priority", "whenever", "no rush"]

  task_reference:
    type: reference
    resolution:
      - exact_match: "title equals input"
      - fuzzy_match: "title contains input"
      - ordinal: "first", "second", "last"
      - recency: "most recent", "latest"
```

## Response Templates

### Success Responses
```yaml
success_responses:
  task_created:
    template: |
      ✅ Created: "{title}"
      {details}
    details_template: |
      📅 Due: {due_date}
      🔴 Priority: {priority}
      🏷️ Tags: {tags}
    suggestions:
      - "Show my tasks"
      - "Add another task"

  task_completed:
    template: |
      ✅ Nice work! Marked "{title}" as complete.
    suggestions:
      - "Show remaining tasks"
      - "What's next?"

  task_deleted:
    template: |
      🗑️ Deleted "{title}"
    suggestions:
      - "Show my tasks"
      - "Undo" # if supported

  tasks_listed:
    template: |
      📋 {description}:

      {task_list}

      {summary}
    task_list_item: |
      {status_icon} {title}{due_info}{priority_icon}
    summary: |
      Total: {total} | Pending: {pending} | Completed: {completed}
```

### Error Responses
```yaml
error_responses:
  task_not_found:
    template: |
      I couldn't find a task matching "{query}".
    suggestions:
      - "Show my tasks"
      - "Create a new task"

  ambiguous_reference:
    template: |
      I found multiple tasks matching "{query}":
      {for task in matches}
      {index}. {task.title}
      {/for}
      Which one did you mean? (Reply with the number)

  missing_info:
    template: |
      I need more information to {action}.
      {missing_field_prompt}
    field_prompts:
      task_title: "What would you like to call the task?"
      due_date: "When should this be due?"

  auth_required:
    template: |
      You'll need to log in to manage tasks.
    suggestions:
      - "Log in"
      - "Create account"

  generic_error:
    template: |
      Something went wrong. Please try again.
    suggestions:
      - "Show my tasks"
      - "Help"
```

### Clarification Responses
```yaml
clarification_responses:
  confirm_delete:
    template: |
      Are you sure you want to delete "{title}"?
    options:
      - "Yes, delete it"
      - "No, keep it"

  confirm_update:
    template: |
      Update "{title}" - change {field} to "{new_value}"?
    options:
      - "Yes"
      - "No"

  disambiguate_task:
    template: |
      Which task do you mean?
      {for task in options}
      {index}. {task.title}
      {/for}
```

## Conversation State Machine

```yaml
states:
  idle:
    description: "Waiting for user input"
    transitions:
      - on: any_intent
        to: processing

  processing:
    description: "Processing user request"
    transitions:
      - on: success
        to: idle
      - on: needs_clarification
        to: clarifying
      - on: needs_confirmation
        to: confirming

  clarifying:
    description: "Asking for more information"
    context:
      - original_intent
      - missing_fields
    transitions:
      - on: user_response
        to: processing
      - on: cancel
        to: idle

  confirming:
    description: "Waiting for user confirmation"
    context:
      - pending_action
      - action_details
    transitions:
      - on: confirm
        to: processing
      - on: deny
        to: idle
```

## Usage Examples

### Process Create Task Message
```
Input: "Add buy milk to my list for tomorrow"

Processing:
1. Intent: create_task
2. Entities:
   - task_title: "buy milk"
   - due_date: "tomorrow" → 2024-01-16
3. Execute: taskService.create({...})
4. Response: "✅ Created: 'buy milk'\n📅 Due: Tomorrow"
5. Suggestions: ["Show my tasks", "Add another task"]
```

### Process List Tasks Message
```
Input: "What do I have to do today?"

Processing:
1. Intent: list_tasks
2. Entities:
   - date_filter: "today"
3. Execute: taskService.list({dueDate: today})
4. Response with formatted task list
5. Suggestions based on task count
```

### Handle Ambiguous Reference
```
Input: "Complete the shopping task"

Processing:
1. Intent: complete_task
2. Entity: task_reference = "shopping"
3. Found: ["grocery shopping", "shopping for gifts"]
4. State: clarifying
5. Response: "Which task do you mean?\n1. grocery shopping\n2. shopping for gifts"
```

## Integration Points

- Works with NLP-Task-Handler for intent extraction
- Integrates with FastAPI-Endpoint-Generator for task operations
- Coordinates with Task-Coordinator for efficient execution
- Uses Todo-NLP-Processor agent for complex NLP tasks
