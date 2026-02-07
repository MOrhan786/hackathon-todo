---
name: task-reminder-agent
description: "Manage task reminders and due date notifications. Integrates recurring task handling and reminders into chatbot interactions for proactive task management."
version: "1.0.0"
used_by:
  - Task Scheduler Agent
  - Chatbot AI Agent
tags:
  - reminders
  - notifications
  - scheduling
  - chatbot
---

# Task Reminder Agent Skill

## Purpose

Manage task reminders and due date notifications to help users stay on top of their tasks. This skill integrates recurring task handling and reminder systems into chatbot interactions for proactive task management.

## Capabilities

### 1. Reminder Scheduling
- Schedule reminders for task due dates
- Set custom reminder times
- Create multiple reminders per task
- Handle timezone considerations

### 2. Recurring Task Management
- Create recurring task patterns
- Generate task instances from patterns
- Handle exceptions and skips
- Manage series modifications

### 3. Notification Delivery
- Send reminder notifications
- Format notification content
- Handle delivery channels
- Track delivery status

### 4. Chatbot Integration
- Process reminder-related commands
- Provide proactive reminders in chat
- Allow reminder management via conversation
- Surface upcoming deadlines

### 5. Smart Scheduling
- Suggest optimal reminder times
- Avoid notification overload
- Group related reminders
- Adapt to user patterns

## Reminder Configuration

### Reminder Types
```yaml
reminder_types:
  due_date_reminder:
    description: "Remind before task is due"
    default_timing:
      - "1 day before"
      - "1 hour before"
    customizable: true

  recurring_reminder:
    description: "Remind at regular intervals"
    patterns:
      - "every day at 9am"
      - "every monday"
      - "every month on the 1st"

  follow_up_reminder:
    description: "Remind to check on task progress"
    trigger: "task in_progress for > 24h"

  overdue_reminder:
    description: "Remind about overdue tasks"
    frequency: "daily until completed"
```

### Timing Options
```yaml
timing_options:
  relative_to_due_date:
    - "at_time": "At the due time"
    - "15_minutes": "15 minutes before"
    - "30_minutes": "30 minutes before"
    - "1_hour": "1 hour before"
    - "2_hours": "2 hours before"
    - "1_day": "1 day before"
    - "2_days": "2 days before"
    - "1_week": "1 week before"

  specific_time:
    format: "HH:MM"
    timezone: "user_local"

  smart_timing:
    - "morning": "9:00 AM"
    - "afternoon": "2:00 PM"
    - "evening": "6:00 PM"
```

## Recurring Task Patterns

### Pattern Definitions
```yaml
recurrence_patterns:
  daily:
    pattern: "FREQ=DAILY"
    examples:
      - "every day"
      - "daily"
      - "every day at 9am"
    parameters:
      interval: 1  # every N days
      time: optional

  weekly:
    pattern: "FREQ=WEEKLY"
    examples:
      - "every week"
      - "every monday"
      - "every mon, wed, fri"
    parameters:
      interval: 1  # every N weeks
      days: ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

  monthly:
    pattern: "FREQ=MONTHLY"
    examples:
      - "every month"
      - "on the 1st of every month"
      - "on the last friday of each month"
    parameters:
      interval: 1  # every N months
      day_of_month: 1-31 or "last"
      day_of_week: optional (for "first monday" etc.)

  yearly:
    pattern: "FREQ=YEARLY"
    examples:
      - "every year"
      - "every january 1st"
    parameters:
      interval: 1
      month: 1-12
      day: 1-31

  custom:
    pattern: "FREQ=CUSTOM"
    examples:
      - "every 2 weeks"
      - "every 3 months"
      - "every other day"
```

### Pattern Parsing
```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum

class RecurrenceFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

@dataclass
class RecurrencePattern:
    frequency: RecurrenceFrequency
    interval: int = 1
    days_of_week: Optional[List[int]] = None  # 0=Monday, 6=Sunday
    day_of_month: Optional[int] = None
    month: Optional[int] = None
    time: Optional[str] = None  # HH:MM format
    end_date: Optional[datetime] = None
    count: Optional[int] = None  # Max occurrences

    def get_next_occurrence(self, after: datetime) -> Optional[datetime]:
        """Calculate the next occurrence after the given datetime."""
        # Implementation varies by frequency
        pass

    def get_occurrences(
        self,
        start: datetime,
        end: datetime
    ) -> List[datetime]:
        """Get all occurrences between start and end dates."""
        occurrences = []
        current = start
        while current <= end:
            next_occ = self.get_next_occurrence(current)
            if next_occ and next_occ <= end:
                occurrences.append(next_occ)
                current = next_occ + timedelta(minutes=1)
            else:
                break
        return occurrences
```

## Notification System

### Notification Service
```python
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class NotificationChannel(str, Enum):
    CHATBOT = "chatbot"
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"

class NotificationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Notification:
    id: str
    user_id: int
    task_id: int
    channel: NotificationChannel
    priority: NotificationPriority
    title: str
    body: str
    scheduled_for: datetime
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class ReminderService:
    """Service for managing task reminders."""

    async def schedule_reminder(
        self,
        task_id: int,
        user_id: int,
        remind_at: datetime,
        channel: NotificationChannel = NotificationChannel.CHATBOT
    ) -> Notification:
        """Schedule a reminder for a task."""
        task = await self.task_service.get_task(task_id)

        notification = Notification(
            id=generate_id(),
            user_id=user_id,
            task_id=task_id,
            channel=channel,
            priority=self._get_priority(task),
            title=f"Reminder: {task.title}",
            body=self._format_reminder_body(task),
            scheduled_for=remind_at
        )

        await self.notification_repository.save(notification)
        await self.scheduler.schedule(notification)

        return notification

    async def process_due_reminders(self):
        """Process all reminders that are due."""
        now = datetime.utcnow()
        due_reminders = await self.notification_repository.get_pending(
            before=now
        )

        for reminder in due_reminders:
            await self._send_notification(reminder)

    async def _send_notification(self, notification: Notification):
        """Send notification through appropriate channel."""
        if notification.channel == NotificationChannel.CHATBOT:
            await self.chatbot_service.send_proactive_message(
                user_id=notification.user_id,
                message=self._format_chatbot_reminder(notification)
            )
        # Handle other channels...

        notification.sent_at = datetime.utcnow()
        await self.notification_repository.update(notification)
```

### Chatbot Reminder Messages
```yaml
chatbot_reminders:
  upcoming_task:
    template: |
      ⏰ Reminder: "{task_title}" is due {time_description}
      {if description}
      📝 {description}
      {/if}
    suggestions:
      - "Mark as complete"
      - "Snooze 1 hour"
      - "View task details"

  overdue_task:
    template: |
      ⚠️ Overdue: "{task_title}" was due {time_ago}
    suggestions:
      - "Mark as complete"
      - "Update due date"
      - "Delete task"

  daily_summary:
    template: |
      📋 Good morning! Here's your day:

      Due Today ({count}):
      {for task in today_tasks}
      • {task.title} {if task.time}at {task.time}{/if}
      {/for}

      {if overdue_count > 0}
      ⚠️ You also have {overdue_count} overdue task(s)
      {/if}
    suggestions:
      - "Show all tasks"
      - "What's most urgent?"

  recurring_task_created:
    template: |
      🔄 Recurring task created: "{task_title}"
      Schedule: {recurrence_description}
      Next occurrence: {next_date}
    suggestions:
      - "Show all recurring tasks"
      - "Edit schedule"
```

## Chatbot Commands

### Reminder Commands
```yaml
commands:
  set_reminder:
    patterns:
      - "remind me about {task} {time}"
      - "set a reminder for {task}"
      - "notify me {time} before {task}"
    examples:
      - "Remind me about the meeting in 30 minutes"
      - "Set a reminder for grocery shopping tomorrow morning"
    response: "I'll remind you about '{task}' {time_description}"

  list_reminders:
    patterns:
      - "show my reminders"
      - "what reminders do I have"
      - "upcoming reminders"
    response: "Here are your upcoming reminders: ..."

  cancel_reminder:
    patterns:
      - "cancel reminder for {task}"
      - "remove reminder"
      - "don't remind me about {task}"
    response: "Reminder cancelled for '{task}'"

  snooze:
    patterns:
      - "snooze"
      - "remind me later"
      - "snooze for {duration}"
    default_duration: "1 hour"
    response: "I'll remind you again in {duration}"

  create_recurring:
    patterns:
      - "create recurring task {task} {pattern}"
      - "add {task} every {pattern}"
      - "remind me to {task} {pattern}"
    examples:
      - "Create recurring task: team standup every weekday at 9am"
      - "Add water plants every sunday"
    response: "Created recurring task: '{task}' - {pattern_description}"
```

## Smart Features

### Intelligent Reminder Suggestions
```yaml
smart_suggestions:
  based_on_task_type:
    meeting:
      suggest: "15 minutes before"
      reason: "Preparation time"

    deadline:
      suggest: "1 day before"
      reason: "Buffer for completion"

    recurring:
      suggest: "At scheduled time"
      reason: "Consistent timing"

  based_on_priority:
    urgent:
      suggest: "Multiple reminders"
      pattern: ["1 day before", "2 hours before", "30 minutes before"]

    high:
      suggest: "1 day and 1 hour before"

    normal:
      suggest: "1 day before"

    low:
      suggest: "Same day morning"

  based_on_user_behavior:
    frequently_snoozed:
      adjust: "Send earlier"
      reason: "User often needs more time"

    quickly_completed:
      adjust: "Send closer to due time"
      reason: "User completes quickly"
```

### Reminder Grouping
```yaml
grouping:
  daily_digest:
    time: "9:00 AM user local"
    include:
      - tasks due today
      - overdue tasks
      - upcoming important tasks
    max_items: 5

  evening_preview:
    time: "6:00 PM user local"
    include:
      - tasks due tomorrow
      - incomplete today tasks
    condition: "if any qualifying tasks"
```

## Usage Examples

### Schedule Task Reminder
```
Input: "Remind me about the report 1 hour before"

Processing:
1. Find task matching "report"
2. Get task due date
3. Calculate reminder time (due_date - 1 hour)
4. Schedule notification
5. Confirm to user

Output: "I'll remind you about 'Quarterly Report' at 2:00 PM (1 hour before it's due)"
```

### Create Recurring Task
```
Input: "Add water plants every Sunday at 10am"

Processing:
1. Create task: "Water plants"
2. Set recurrence: WEEKLY on SU at 10:00
3. Generate first occurrence
4. Schedule reminder

Output: "Created recurring task: 'Water plants' every Sunday at 10:00 AM. Next: This Sunday"
```

### Daily Summary
```
Trigger: 9:00 AM user local time

Output:
"Good morning! Here's your day:

Due Today (3):
• Team standup at 9:30 AM
• Submit expense report
• Call client at 2:00 PM

You also have 1 overdue task"
```

## Integration Points

- Works with Recurring-Task-Scheduler agent for complex patterns
- Integrates with Chatbot-Response-Handler for notifications
- Uses Task-Coordinator for task operations
- Coordinates with Todo-NLP-Processor for command parsing
