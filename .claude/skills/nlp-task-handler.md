---
name: nlp-task-handler
description: "Enable natural language processing for task management. Processes and understands task-related commands in natural language for intuitive chatbot interactions."
version: "1.0.0"
used_by:
  - Chatbot AI Agent
tags:
  - nlp
  - natural-language
  - task-management
  - chatbot
---

# NLP Task Handler Skill

## Purpose

Enable natural language processing for task management operations. This skill processes and understands task-related commands in natural language, allowing users to manage tasks through intuitive conversation with the chatbot.

## Capabilities

### 1. Intent Classification
- Classify user messages into task intents
- Handle multi-intent messages
- Detect implicit intents
- Score confidence levels

### 2. Entity Extraction
- Extract task-related entities
- Parse dates and times
- Identify task references
- Handle entity synonyms

### 3. Context Understanding
- Maintain conversation context
- Resolve pronouns and references
- Handle follow-up questions
- Manage topic switches

### 4. Language Variations
- Handle typos and misspellings
- Process informal language
- Support abbreviations
- Understand colloquialisms

### 5. Command Synthesis
- Convert NL to structured commands
- Validate extracted parameters
- Request missing information
- Confirm interpretations

## Intent Classification

### Intent Definitions
```yaml
intents:
  task_create:
    description: "Create a new task"
    confidence_threshold: 0.7
    training_examples:
      - "add {task} to my list"
      - "create a task for {task}"
      - "I need to {task}"
      - "remind me to {task}"
      - "don't forget to {task}"
      - "put {task} on my todo"
      - "new task: {task}"
      - "add task {task}"

  task_complete:
    description: "Mark task as complete"
    confidence_threshold: 0.75
    training_examples:
      - "mark {task} as done"
      - "complete {task}"
      - "I finished {task}"
      - "done with {task}"
      - "{task} is complete"
      - "check off {task}"
      - "I did {task}"

  task_delete:
    description: "Delete a task"
    confidence_threshold: 0.8
    training_examples:
      - "delete {task}"
      - "remove {task}"
      - "cancel {task}"
      - "get rid of {task}"
      - "I don't need {task} anymore"

  task_list:
    description: "View tasks"
    confidence_threshold: 0.7
    training_examples:
      - "show my tasks"
      - "what do I have to do"
      - "list all tasks"
      - "what's on my list"
      - "my todos"
      - "show me everything"
      - "what needs to be done"

  task_update:
    description: "Modify a task"
    confidence_threshold: 0.75
    training_examples:
      - "change {task} to {new_value}"
      - "update {task}"
      - "rename {task} to {new_name}"
      - "set {task} priority to {priority}"
      - "move {task} to {date}"
      - "change the deadline for {task}"

  task_search:
    description: "Find specific tasks"
    confidence_threshold: 0.7
    training_examples:
      - "find {query}"
      - "search for {query}"
      - "where is {query}"
      - "do I have a task about {query}"
      - "tasks related to {query}"

  task_query:
    description: "Ask about tasks"
    confidence_threshold: 0.7
    training_examples:
      - "what's due today"
      - "how many tasks do I have"
      - "what's most urgent"
      - "am I free tomorrow"
      - "what's next"
      - "any overdue tasks"

  greeting:
    description: "Greeting or small talk"
    confidence_threshold: 0.8
    training_examples:
      - "hello"
      - "hi"
      - "hey"
      - "good morning"
      - "how are you"

  help:
    description: "Request assistance"
    confidence_threshold: 0.75
    training_examples:
      - "help"
      - "what can you do"
      - "how do I use this"
      - "commands"
      - "options"
```

### Classification Algorithm
```python
from dataclasses import dataclass
from typing import List, Tuple, Optional
import re

@dataclass
class IntentResult:
    intent: str
    confidence: float
    entities: dict
    raw_text: str

class IntentClassifier:
    """Classify user messages into intents."""

    def __init__(self):
        self.intent_patterns = self._load_patterns()
        self.keyword_weights = self._load_keywords()

    def classify(self, text: str) -> IntentResult:
        """Classify a user message."""
        normalized = self._normalize(text)

        # Score each intent
        scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = self._calculate_intent_score(normalized, patterns)
            scores[intent] = score

        # Get best match
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]

        # Extract entities
        entities = self._extract_entities(normalized, best_intent)

        return IntentResult(
            intent=best_intent,
            confidence=confidence,
            entities=entities,
            raw_text=text
        )

    def _normalize(self, text: str) -> str:
        """Normalize text for processing."""
        text = text.lower().strip()
        # Remove punctuation except apostrophes
        text = re.sub(r"[^\w\s']", " ", text)
        # Normalize whitespace
        text = " ".join(text.split())
        return text

    def _calculate_intent_score(
        self,
        text: str,
        patterns: List[dict]
    ) -> float:
        """Calculate confidence score for an intent."""
        max_score = 0.0

        for pattern in patterns:
            # Pattern matching
            if pattern.get("regex"):
                if re.search(pattern["regex"], text):
                    max_score = max(max_score, pattern.get("weight", 0.8))

            # Keyword matching
            if pattern.get("keywords"):
                keyword_score = self._keyword_match_score(
                    text,
                    pattern["keywords"]
                )
                max_score = max(max_score, keyword_score)

        return max_score

    def _keyword_match_score(
        self,
        text: str,
        keywords: List[Tuple[str, float]]
    ) -> float:
        """Score based on keyword presence."""
        total_weight = 0.0
        matched_weight = 0.0

        for keyword, weight in keywords:
            total_weight += weight
            if keyword in text:
                matched_weight += weight

        if total_weight == 0:
            return 0.0

        return matched_weight / total_weight
```

## Entity Extraction

### Entity Types
```yaml
entities:
  task_title:
    type: "free_text"
    extraction_patterns:
      - regex: "(?:add|create|new task)[:\s]+(.+?)(?:\s+(?:by|due|for|tomorrow|today)|$)"
      - regex: "(?:remind me to|don't forget to)\s+(.+?)(?:\s+(?:by|at|tomorrow|today)|$)"
      - regex: "I need to\s+(.+?)(?:\s+(?:by|before)|$)"
    post_processing:
      - strip_filler_words
      - capitalize_first

  due_date:
    type: "datetime"
    extraction_patterns:
      # Relative dates
      - regex: "(today|tomorrow|tonight)"
        resolve: "relative"
      - regex: "(next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month)"
        resolve: "relative"
      - regex: "in\s+(\d+)\s+(days?|weeks?|months?|hours?)"
        resolve: "relative"

      # Absolute dates
      - regex: "(\d{1,2})[/\-](\d{1,2})(?:[/\-](\d{2,4}))?"
        resolve: "absolute"
      - regex: "(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(?:st|nd|rd|th)?(?:\s*,?\s*(\d{4}))?"
        resolve: "absolute"

      # Time expressions
      - regex: "(?:at|by)\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?"
        resolve: "time"

  priority:
    type: "enum"
    values: ["low", "medium", "high", "urgent"]
    extraction_patterns:
      - regex: "(?:priority|important(?:ance)?)[:\s]*(low|medium|high|urgent)"
      - keywords:
          urgent: ["urgent", "asap", "immediately", "critical", "emergency"]
          high: ["important", "high priority", "priority", "crucial"]
          low: ["low priority", "whenever", "no rush", "not urgent"]
    default: "medium"

  task_reference:
    type: "reference"
    extraction_patterns:
      - regex: "(?:the|my|that)\s+(.+?)\s+task"
      - regex: "task\s+(?:called|named|about)\s+(.+?)(?:\s|$)"
      - ordinal: "first|second|third|last|next"
      - position: "#(\d+)"
    resolution:
      - exact_title_match
      - fuzzy_title_match
      - keyword_search
      - ordinal_position

  status_filter:
    type: "enum"
    values: ["pending", "in_progress", "completed", "all"]
    extraction_patterns:
      - keywords:
          pending: ["pending", "todo", "not done", "incomplete", "remaining"]
          in_progress: ["in progress", "working on", "started"]
          completed: ["done", "completed", "finished", "complete"]
          all: ["all", "everything", "all tasks"]

  tags:
    type: "list"
    extraction_patterns:
      - regex: "#(\w+)"
      - regex: "(?:tag(?:ged)?|label(?:ed)?)[:\s]+(.+?)(?:\s+and\s+|\s*,\s*|$)"
```

### Date/Time Parser
```python
from datetime import datetime, timedelta
from typing import Optional
import re

class DateTimeParser:
    """Parse natural language date/time expressions."""

    WEEKDAYS = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }

    MONTHS = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12
    }

    def parse(self, text: str, reference: datetime = None) -> Optional[datetime]:
        """Parse date/time from text."""
        if reference is None:
            reference = datetime.now()

        text = text.lower().strip()

        # Try relative dates
        if result := self._parse_relative(text, reference):
            return result

        # Try weekday references
        if result := self._parse_weekday(text, reference):
            return result

        # Try absolute dates
        if result := self._parse_absolute(text, reference):
            return result

        return None

    def _parse_relative(self, text: str, ref: datetime) -> Optional[datetime]:
        """Parse relative date expressions."""
        if text == "today":
            return ref.replace(hour=23, minute=59)

        if text == "tomorrow":
            return (ref + timedelta(days=1)).replace(hour=23, minute=59)

        if text == "tonight":
            return ref.replace(hour=21, minute=0)

        # "in X days/weeks/months"
        match = re.match(r"in\s+(\d+)\s+(day|week|month|hour)s?", text)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            if unit == "day":
                return ref + timedelta(days=amount)
            elif unit == "week":
                return ref + timedelta(weeks=amount)
            elif unit == "month":
                return ref + timedelta(days=amount * 30)
            elif unit == "hour":
                return ref + timedelta(hours=amount)

        return None

    def _parse_weekday(self, text: str, ref: datetime) -> Optional[datetime]:
        """Parse weekday references."""
        for day_name, day_num in self.WEEKDAYS.items():
            if day_name in text:
                days_ahead = day_num - ref.weekday()
                if "next" in text:
                    days_ahead += 7
                elif days_ahead <= 0:
                    days_ahead += 7
                return (ref + timedelta(days=days_ahead)).replace(hour=23, minute=59)
        return None

    def _parse_absolute(self, text: str, ref: datetime) -> Optional[datetime]:
        """Parse absolute date expressions."""
        # MM/DD or MM/DD/YYYY
        match = re.match(r"(\d{1,2})[/\-](\d{1,2})(?:[/\-](\d{2,4}))?", text)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            year = int(match.group(3)) if match.group(3) else ref.year
            if year < 100:
                year += 2000
            try:
                return datetime(year, month, day, 23, 59)
            except ValueError:
                pass

        # Month Day (Year)
        for month_name, month_num in self.MONTHS.items():
            if month_name in text:
                match = re.search(rf"{month_name}\s+(\d{{1,2}})(?:\s*,?\s*(\d{{4}}))?", text)
                if match:
                    day = int(match.group(1))
                    year = int(match.group(2)) if match.group(2) else ref.year
                    try:
                        return datetime(year, month_num, day, 23, 59)
                    except ValueError:
                        pass

        return None
```

## Context Management

### Conversation Context
```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class ConversationContext:
    """Maintain context across conversation turns."""

    session_id: str
    user_id: Optional[int]

    # Current conversation state
    current_intent: Optional[str] = None
    pending_action: Optional[Dict[str, Any]] = None
    awaiting_input: Optional[str] = None

    # Reference tracking
    last_mentioned_task: Optional[int] = None
    last_mentioned_tasks: List[int] = field(default_factory=list)
    last_query_results: List[int] = field(default_factory=list)

    # Conversation history
    recent_intents: List[str] = field(default_factory=list)
    recent_entities: Dict[str, Any] = field(default_factory=dict)

    # Timestamps
    last_activity: datetime = field(default_factory=datetime.utcnow)
    session_start: datetime = field(default_factory=datetime.utcnow)

    def update_intent(self, intent: str, entities: Dict[str, Any]):
        """Update context with new intent."""
        self.current_intent = intent
        self.recent_intents.append(intent)
        if len(self.recent_intents) > 10:
            self.recent_intents.pop(0)

        self.recent_entities.update(entities)
        self.last_activity = datetime.utcnow()

    def set_pending_action(self, action: Dict[str, Any]):
        """Set a pending action awaiting confirmation."""
        self.pending_action = action

    def clear_pending_action(self):
        """Clear pending action after completion or cancellation."""
        self.pending_action = None

    def resolve_reference(self, reference: str) -> Optional[int]:
        """Resolve a task reference using context."""
        reference = reference.lower()

        # Pronouns
        if reference in ["it", "that", "this", "the task"]:
            return self.last_mentioned_task

        # Ordinals
        if reference in ["first", "1st"] and self.last_query_results:
            return self.last_query_results[0]
        if reference in ["last"] and self.last_query_results:
            return self.last_query_results[-1]

        # Position
        if match := re.match(r"(?:#|number\s*)(\d+)", reference):
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(self.last_query_results):
                return self.last_query_results[idx]

        return None
```

## Usage Examples

### Process Natural Language Input
```
Input: "remind me to buy milk tomorrow morning"

Processing:
1. Normalize: "remind me to buy milk tomorrow morning"
2. Classify intent: task_create (confidence: 0.92)
3. Extract entities:
   - task_title: "buy milk"
   - due_date: "tomorrow morning" → 2024-01-16 09:00
4. Synthesize command:
   {
     "action": "create_task",
     "title": "Buy milk",
     "due_date": "2024-01-16T09:00:00",
     "reminder": "2024-01-16T08:30:00"
   }

Output: "Created task: 'Buy milk' due tomorrow at 9:00 AM"
```

### Handle Ambiguous Input
```
Input: "what about the report"

Processing:
1. Classify: Ambiguous - could be query or reference
2. Check context:
   - Last intent: task_list
   - Last mentioned: "quarterly report" task
3. Infer: User asking about previously mentioned task
4. Response: Show details for "quarterly report"

Output: "'Quarterly Report' - Due Friday, Priority: High"
```

### Multi-Intent Processing
```
Input: "add buy groceries and mark the laundry task as done"

Processing:
1. Detect multi-intent message
2. Split: ["add buy groceries", "mark the laundry task as done"]
3. Process each:
   - Intent 1: task_create, title: "buy groceries"
   - Intent 2: task_complete, reference: "laundry task"
4. Execute both actions
5. Combined response

Output: "Done! Created 'Buy groceries' and marked 'Do laundry' as complete"
```

## Integration Points

- Works with Chatbot-Response-Handler for response generation
- Integrates with Task-Coordinator for task operations
- Uses Todo-NLP-Processor agent for complex NLP tasks
- Coordinates with Task-Reminder-Agent for scheduling
